"""
explanation.py
--------------
Generates human-readable explanations for a diagnosis.
Answers: WHY was this disease diagnosed?
"""

from core.inference_engine import DiagnosisResult


class ExplanationModule:
    """
    Takes a DiagnosisResult and produces a
    clear, readable explanation of the reasoning.
    """

    def __init__(self, result: DiagnosisResult, all_symptoms: list):
        self.result = result
        self.all_symptoms = all_symptoms  # all symptoms the patient reported

    def get_full_explanation(self) -> str:
        r = self.result
        lines = []

        lines.append(f"DIAGNOSIS: {r.display_name}")
        lines.append(f"Confidence: {r.confidence}%")
        lines.append(f"Severity  : {r.severity.upper()}")
        lines.append("")
        lines.append(f"Description: {r.description}")
        lines.append("")
        lines.append("WHY THIS DIAGNOSIS?")
        lines.append(f"  {len(r.fired_rules)} rule(s) fired for this disease.")
        lines.append("")

        for i, rule in enumerate(r.fired_rules, 1):
            lines.append(f"  Rule {i}: [{rule.rule_id}]")
            lines.append(f"    Matched symptoms : {', '.join(rule.matched_conditions)}")
            lines.append(f"    Reasoning        : {rule.explanation}")
            lines.append(f"    Confidence added : +{rule.confidence_boost}")
            lines.append("")

        lines.append(f"Key symptoms that contributed: {', '.join(r.matched_symptoms)}")
        lines.append("")
        lines.append(f"RECOMMENDED ACTION: {r.recommended_action}")

        return "\n".join(lines)

    def get_short_explanation(self) -> str:
        """One-liner explanation for quick display."""
        rule_ids = [r.rule_id for r in self.result.fired_rules]
        return (
            f"{self.result.display_name} diagnosed with {self.result.confidence}% confidence "
            f"based on rules {', '.join(rule_ids)} "
            f"matching symptoms: {', '.join(self.result.matched_symptoms)}."
        )