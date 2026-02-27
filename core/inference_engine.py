"""
inference_engine.py
-------------------
The brain of the expert system.

How it works:
  1. Takes all facts from WorkingMemory
  2. Checks every Rule in KnowledgeBase
  3. If ALL conditions of a rule match -> rule FIRES
  4. Fired rules add confidence to their disease
  5. Diseases are ranked by total confidence
  6. Returns ranked diagnoses + explanation of which rules fired

Forward Chaining:
  Start with FACTS (symptoms) -> match RULES -> conclude DISEASES
"""

import json
import os
from collections import defaultdict
from dataclasses import dataclass

from core.knowledge_base import KnowledgeBase, Rule
from core.working_memory import WorkingMemory


# ── Load disease metadata ────────────────────

def _load_disease_data() -> dict:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "data", "diseases.json")
    with open(path) as f:
        return json.load(f)


# ── Result Dataclasses ───────────────────────

@dataclass
class FiredRule:
    """A rule that fired during inference."""
    rule_id: str
    disease: str
    matched_conditions: list
    confidence_boost: float
    severity: str
    explanation: str


@dataclass
class DiagnosisResult:
    """A single disease diagnosis with confidence and metadata."""
    disease: str
    display_name: str
    confidence: float           # 0.0 to 100.0
    severity: str
    recommended_action: str
    fired_rules: list
    matched_symptoms: list
    description: str


# ── Inference Engine ─────────────────────────

class InferenceEngine:
    """
    Core reasoning engine using forward chaining.

    Usage:
        engine = InferenceEngine(knowledge_base, working_memory)
        results = engine.run()
    """

    def __init__(self, kb: KnowledgeBase, wm: WorkingMemory):
        self.kb = kb
        self.wm = wm
        self.disease_data = _load_disease_data()
        self._fired_rules = []
        self._confidence_map = defaultdict(float)
        self._matched_symptoms_map = defaultdict(set)

    def run(self) -> list:
        """
        Run forward chaining inference.
        Returns list of DiagnosisResult sorted by confidence (highest first).
        """
        # Reset state
        self._fired_rules.clear()
        self._confidence_map.clear()
        self._matched_symptoms_map.clear()

        # Step 1: Match every rule against working memory
        for rule in self.kb.get_all_rules():
            if self._rule_matches(rule):
                self._fire_rule(rule)

        # Step 2: If nothing fired, return empty
        if not self._confidence_map:
            return []

        # Step 3: Build and sort results
        results = self._build_results()
        results.sort(key=lambda x: x.confidence, reverse=True)

        return results

    def _rule_matches(self, rule: Rule) -> bool:
        """Check if ALL conditions of a rule exist in working memory."""
        return all(self.wm.has_symptom(cond) for cond in rule.conditions)

    def _fire_rule(self, rule: Rule):
        """Fire a rule — log it and accumulate confidence."""
        fired = FiredRule(
            rule_id=rule.rule_id,
            disease=rule.disease,
            matched_conditions=rule.conditions,
            confidence_boost=rule.confidence_boost,
            severity=rule.severity,
            explanation=rule.explanation
        )
        self._fired_rules.append(fired)
        self._confidence_map[rule.disease] += rule.confidence_boost
        for symptom in rule.conditions:
            self._matched_symptoms_map[rule.disease].add(symptom)

    def _build_results(self) -> list:
        """Convert confidence map into DiagnosisResult objects."""
        total_confidence = sum(self._confidence_map.values())
        results = []
        diseases_info = self.disease_data["diseases"]

        for disease, raw_confidence in self._confidence_map.items():
            confidence_pct = round((raw_confidence / total_confidence) * 100, 1)
            confidence_pct = min(confidence_pct, 85.0)  # cap at 85% — more realistic
            info = diseases_info.get(disease, {})
            disease_fired_rules = [fr for fr in self._fired_rules if fr.disease == disease]
            severity = self._resolve_severity(disease_fired_rules, info.get("severity", "low"))

            result = DiagnosisResult(
                disease=disease,
                display_name=info.get("display_name", disease),
                confidence=confidence_pct,
                severity=severity,
                recommended_action=info.get("recommended_action", "Consult a doctor."),
                fired_rules=disease_fired_rules,
                matched_symptoms=sorted(list(self._matched_symptoms_map[disease])),
                description=info.get("description", "")
            )
            results.append(result)

        return results

    def _resolve_severity(self, fired_rules: list, default: str) -> str:
        """Use highest severity among all fired rules for this disease."""
        priority = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        max_severity = default
        for rule in fired_rules:
            if priority.get(rule.severity, 0) > priority.get(max_severity, 0):
                max_severity = rule.severity
        return max_severity

    def get_fired_rules(self) -> list:
        """Return all rules that fired in the last run."""
        return self._fired_rules

    def get_top_diagnosis(self):
        """Returns only the top diagnosis."""
        results = self.run()
        return results[0] if results else None