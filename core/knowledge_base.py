"""
knowledge_base.py
-----------------
Defines the Rule dataclass and KnowledgeBase class.
All medical rules for the expert system are encoded here.

Diseases covered:
  - Common Flu
  - Dengue Fever
  - Malaria
  - Typhoid Fever

Rule design:
  - Each rule has a set of CONDITIONS (symptoms).
  - If ALL conditions match the patient's facts, the rule FIRES.
  - Each rule contributes a confidence_boost (float) to its disease.
  - Multiple rules can fire for the same disease → confidence accumulates.
  - The inference engine ranks diseases by total accumulated confidence.
"""

from dataclasses import dataclass


# ── Rule Dataclass ───────────────────────────

@dataclass
class Rule:
    """
    Represents a single IF-THEN diagnostic rule.

    Attributes:
        rule_id         : Unique identifier (e.g., "R01")
        conditions      : List of symptoms that must ALL be present
        disease         : Disease this rule supports
        confidence_boost: How much confidence (0–100 scale) this rule adds
        severity        : Severity level if this rule fires (low/medium/high/critical)
        explanation     : Human-readable explanation of why this rule fires
    """
    rule_id: str
    conditions: list
    disease: str
    confidence_boost: float
    severity: str
    explanation: str


# ── KnowledgeBase Class ──────────────────────

class KnowledgeBase:
    """
    Stores and manages all diagnostic rules.
    Acts as the long-term memory of the expert system.
    """

    def __init__(self):
        self.rules: list[Rule] = []
        self._load_rules()

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def get_all_rules(self) -> list[Rule]:
        return self.rules

    def get_rules_for_disease(self, disease: str) -> list[Rule]:
        return [r for r in self.rules if r.disease == disease]

    def _load_rules(self):
        """
        Encodes all medical diagnostic rules.
        Rules based on WHO fever guidelines and standard medical references.

        Confidence boost scale:
          5  → weak signal (common symptom, low specificity)
          10 → moderate signal
          15 → strong signal (more specific to this disease)
          20 → very strong / near-pathognomonic signal
        """

        rules = [

            # ── COMMON FLU RULES ─────────────────

            Rule(
                rule_id="R01",
                conditions=["low_grade_fever", "cough", "sore_throat"],
                disease="common_flu",
                confidence_boost=15,
                severity="low",
                explanation="Classic triad of flu: low-grade fever + cough + sore throat strongly suggests influenza."
            ),
            Rule(
                rule_id="R02",
                conditions=["moderate_fever", "runny_nose", "sneezing"],
                disease="common_flu",
                confidence_boost=12,
                severity="low",
                explanation="Runny nose and sneezing with fever are hallmark upper respiratory flu symptoms."
            ),
            Rule(
                rule_id="R03",
                conditions=["moderate_fever", "body_ache", "fatigue"],
                disease="common_flu",
                confidence_boost=12,
                severity="low",
                explanation="Moderate fever with body ache and fatigue is a common flu presentation."
            ),
            Rule(
                rule_id="R04",
                conditions=["moderate_fever", "chills", "headache", "body_ache"],
                disease="common_flu",
                confidence_boost=14,
                severity="low",
                explanation="Chills + headache + body ache with fever is a typical systemic flu response."
            ),
            Rule(
                rule_id="R05",
                conditions=["cough", "sore_throat", "sneezing", "runny_nose"],
                disease="common_flu",
                confidence_boost=10,
                severity="low",
                explanation="Multiple upper respiratory symptoms together point toward influenza."
            ),
            Rule(
                rule_id="R06",
                conditions=["low_grade_fever", "fatigue", "cough"],
                disease="common_flu",
                confidence_boost=8,
                severity="low",
                explanation="Fatigue and cough with low-grade fever is a weak but supportive flu indicator."
            ),

            # ── DENGUE RULES ─────────────────────

            Rule(
                rule_id="R07",
                conditions=["high_fever", "severe_headache", "pain_behind_eyes"],
                disease="dengue",
                confidence_boost=20,
                severity="high",
                explanation="High fever + severe headache + retro-orbital pain is a hallmark dengue triad."
            ),
            Rule(
                rule_id="R08",
                conditions=["high_fever", "joint_pain", "muscle_pain", "rash"],
                disease="dengue",
                confidence_boost=20,
                severity="high",
                explanation="Dengue's 'breakbone fever': high fever + severe joint/muscle pain + rash is strongly diagnostic."
            ),
            Rule(
                rule_id="R09",
                conditions=["high_fever", "rash", "nausea"],
                disease="dengue",
                confidence_boost=15,
                severity="high",
                explanation="Rash with high fever and nausea is a moderate dengue indicator."
            ),
            Rule(
                rule_id="R10",
                conditions=["high_fever", "low_platelet", "mild_bleeding"],
                disease="dengue",
                confidence_boost=20,
                severity="high",
                explanation="Low platelet count with bleeding signs is a critical dengue warning — seek care immediately."
            ),
            Rule(
                rule_id="R11",
                conditions=["high_fever", "pain_behind_eyes", "joint_pain"],
                disease="dengue",
                confidence_boost=18,
                severity="high",
                explanation="Retro-orbital pain + joint pain with high fever is highly specific to dengue."
            ),
            Rule(
                rule_id="R12",
                conditions=["high_fever", "fatigue", "nausea", "vomiting"],
                disease="dengue",
                confidence_boost=10,
                severity="medium",
                explanation="High fever with GI symptoms (nausea/vomiting) and fatigue supports dengue."
            ),
            Rule(
                rule_id="R13",
                conditions=["rash", "joint_pain", "fatigue"],
                disease="dengue",
                confidence_boost=8,
                severity="medium",
                explanation="Rash + joint pain + fatigue without high fever is a weak dengue indicator."
            ),

            # ── MALARIA RULES ────────────────────

            Rule(
                rule_id="R14",
                conditions=["cyclical_fever", "chills", "sweating"],
                disease="malaria",
                confidence_boost=20,
                severity="high",
                explanation="The malaria fever cycle: cyclical fever + chills + profuse sweating is pathognomonic for malaria."
            ),
            Rule(
                rule_id="R15",
                conditions=["high_fever", "shivering", "sweating"],
                disease="malaria",
                confidence_boost=18,
                severity="high",
                explanation="High fever with rigors (shivering) followed by sweating is the classic malaria attack pattern."
            ),
            Rule(
                rule_id="R16",
                conditions=["high_fever", "chills", "headache", "nausea"],
                disease="malaria",
                confidence_boost=15,
                severity="high",
                explanation="Fever + chills + headache + nausea is a common malaria presentation."
            ),
            Rule(
                rule_id="R17",
                conditions=["anemia", "fatigue", "high_fever"],
                disease="malaria",
                confidence_boost=15,
                severity="high",
                explanation="Anemia + fever + fatigue suggests chronic malaria destroying red blood cells."
            ),
            Rule(
                rule_id="R18",
                conditions=["enlarged_spleen", "high_fever", "fatigue"],
                disease="malaria",
                confidence_boost=18,
                severity="high",
                explanation="Splenomegaly (enlarged spleen) with fever is a classic malaria sign."
            ),
            Rule(
                rule_id="R19",
                conditions=["high_fever", "muscle_pain", "vomiting", "chills"],
                disease="malaria",
                confidence_boost=14,
                severity="high",
                explanation="Fever + muscle pain + vomiting + chills together support malaria diagnosis."
            ),
            Rule(
                rule_id="R20",
                conditions=["cyclical_fever", "headache", "fatigue"],
                disease="malaria",
                confidence_boost=12,
                severity="medium",
                explanation="Cyclical fever pattern with headache and fatigue is a moderate malaria indicator."
            ),

            # ── TYPHOID RULES ────────────────────

            Rule(
                rule_id="R21",
                conditions=["sustained_fever", "headache", "abdominal_pain"],
                disease="typhoid",
                confidence_boost=18,
                severity="medium",
                explanation="Sustained (step-ladder) fever + headache + abdominal pain is a classic typhoid presentation."
            ),
            Rule(
                rule_id="R22",
                conditions=["sustained_fever", "loss_of_appetite", "weakness"],
                disease="typhoid",
                confidence_boost=16,
                severity="medium",
                explanation="Prolonged fever with anorexia (loss of appetite) and weakness strongly suggests typhoid."
            ),
            Rule(
                rule_id="R23",
                conditions=["high_fever", "constipation", "abdominal_pain"],
                disease="typhoid",
                confidence_boost=15,
                severity="medium",
                explanation="Fever + constipation + abdominal pain is a common early typhoid symptom cluster."
            ),
            Rule(
                rule_id="R24",
                conditions=["rose_spots", "sustained_fever", "headache"],
                disease="typhoid",
                confidence_boost=20,
                severity="medium",
                explanation="Rose spots (rash on abdomen/chest) with sustained fever is nearly diagnostic of typhoid."
            ),
            Rule(
                rule_id="R25",
                conditions=["slow_heart_rate", "sustained_fever"],
                disease="typhoid",
                confidence_boost=18,
                severity="medium",
                explanation="Relative bradycardia (slow heart rate despite high fever) is a characteristic typhoid sign."
            ),
            Rule(
                rule_id="R26",
                conditions=["enlarged_liver", "sustained_fever", "weakness"],
                disease="typhoid",
                confidence_boost=16,
                severity="medium",
                explanation="Hepatomegaly (enlarged liver) with sustained fever points toward typhoid."
            ),
            Rule(
                rule_id="R27",
                conditions=["diarrhea", "sustained_fever", "abdominal_pain"],
                disease="typhoid",
                confidence_boost=14,
                severity="medium",
                explanation="Diarrhea + sustained fever + abdominal pain is a common late-stage typhoid pattern."
            ),
            Rule(
                rule_id="R28",
                conditions=["headache", "fatigue", "loss_of_appetite", "high_fever"],
                disease="typhoid",
                confidence_boost=12,
                severity="medium",
                explanation="General malaise with high fever can indicate typhoid."
            ),
            Rule(
                rule_id="R29",
                conditions=["high_fever"],
                disease="dengue",
                confidence_boost=5,
                severity="medium",
                explanation="High fever alone is a weak signal that could indicate dengue."
            ),
            Rule(
                rule_id="R30",
                conditions=["high_fever"],
                disease="malaria",
                confidence_boost=5,
                severity="medium",
                explanation="High fever alone is a weak signal that could indicate malaria."
            ),
            Rule(
                rule_id="R31",
                conditions=["high_fever"],
                disease="typhoid",
                confidence_boost=5,
                severity="medium",
                explanation="High fever alone is a weak signal that could indicate typhoid."
            ),
            
            # ── WEAK SIGNAL RULES R32-R40 ────────

            Rule(
                rule_id="R32",
                conditions=["low_grade_fever"],
                disease="common_flu",
                confidence_boost=6,
                severity="low",
                explanation="Low grade fever alone is a weak flu indicator."
            ),
            Rule(
                rule_id="R33",
                conditions=["low_grade_fever", "cough"],
                disease="common_flu",
                confidence_boost=8,
                severity="low",
                explanation="Low grade fever with cough is a moderate flu indicator."
            ),
            Rule(
                rule_id="R34",
                conditions=["low_grade_fever", "sore_throat"],
                disease="common_flu",
                confidence_boost=7,
                severity="low",
                explanation="Low grade fever with sore throat is a moderate flu indicator."
            ),
            Rule(
                rule_id="R35",
                conditions=["low_grade_fever", "body_ache"],
                disease="common_flu",
                confidence_boost=7,
                severity="low",
                explanation="Low grade fever with body ache is a weak flu indicator."
            ),
            Rule(
                rule_id="R36",
                conditions=["low_grade_fever", "headache"],
                disease="common_flu",
                confidence_boost=6,
                severity="low",
                explanation="Low grade fever with headache is a weak flu indicator."
            ),
            Rule(
                rule_id="R37",
                conditions=["low_grade_fever", "chills"],
                disease="common_flu",
                confidence_boost=7,
                severity="low",
                explanation="Low grade fever with chills is a weak flu indicator."
            ),
            Rule(
                rule_id="R38",
                conditions=["low_grade_fever", "fatigue", "body_ache"],
                disease="common_flu",
                confidence_boost=10,
                severity="low",
                explanation="Low grade fever + fatigue + body ache is a common flu presentation."
            ),
            Rule(
                rule_id="R39",
                conditions=["low_grade_fever", "abdominal_pain"],
                disease="typhoid",
                confidence_boost=8,
                severity="medium",
                explanation="Low grade fever with abdominal pain is a weak typhoid indicator."
            ),
            Rule(
                rule_id="R40",
                conditions=["low_grade_fever", "loss_of_appetite"],
                disease="typhoid",
                confidence_boost=7,
                severity="medium",
                explanation="Low grade fever with loss of appetite is a weak typhoid indicator."
            ),
            # ── CATCH-ALL SINGLE SYMPTOM RULES ──────────

            Rule(
                rule_id="R41",
                conditions=["chills"],
                disease="malaria",
                confidence_boost=5,
                severity="medium",
                explanation="Chills alone is a weak malaria indicator."
            ),
            Rule(
                rule_id="R42",
                conditions=["sweating"],
                disease="malaria",
                confidence_boost=5,
                severity="medium",
                explanation="Profuse sweating alone is a weak malaria indicator."
            ),
            Rule(
                rule_id="R43",
                conditions=["cyclical_fever"],
                disease="malaria",
                confidence_boost=8,
                severity="medium",
                explanation="Cyclical fever alone is a moderate malaria indicator."
            ),
            Rule(
                rule_id="R44",
                conditions=["joint_pain"],
                disease="dengue",
                confidence_boost=5,
                severity="medium",
                explanation="Joint pain alone is a weak dengue indicator."
            ),
            Rule(
                rule_id="R45",
                conditions=["pain_behind_eyes"],
                disease="dengue",
                confidence_boost=8,
                severity="medium",
                explanation="Pain behind eyes alone is a moderate dengue indicator."
            ),
            Rule(
                rule_id="R46",
                conditions=["severe_headache"],
                disease="dengue",
                confidence_boost=6,
                severity="medium",
                explanation="Severe headache alone is a weak dengue indicator."
            ),
            Rule(
                rule_id="R47",
                conditions=["rash"],
                disease="dengue",
                confidence_boost=6,
                severity="medium",
                explanation="Skin rash alone is a weak dengue indicator."
            ),
            Rule(
                rule_id="R48",
                conditions=["low_platelet"],
                disease="dengue",
                confidence_boost=8,
                severity="high",
                explanation="Low platelet count alone is a moderate dengue indicator."
            ),
            Rule(
                rule_id="R49",
                conditions=["mild_bleeding"],
                disease="dengue",
                confidence_boost=7,
                severity="high",
                explanation="Mild bleeding alone is a weak dengue indicator."
            ),
            Rule(
                rule_id="R50",
                conditions=["sustained_fever"],
                disease="typhoid",
                confidence_boost=8,
                severity="medium",
                explanation="Sustained fever alone is a moderate typhoid indicator."
            ),
            Rule(
                rule_id="R51",
                conditions=["abdominal_pain"],
                disease="typhoid",
                confidence_boost=6,
                severity="medium",
                explanation="Abdominal pain alone is a weak typhoid indicator."
            ),
            Rule(
                rule_id="R52",
                conditions=["loss_of_appetite"],
                disease="typhoid",
                confidence_boost=5,
                severity="medium",
                explanation="Loss of appetite alone is a weak typhoid indicator."
            ),
            Rule(
                rule_id="R53",
                conditions=["rose_spots"],
                disease="typhoid",
                confidence_boost=10,
                severity="medium",
                explanation="Rose spots alone is a strong typhoid indicator."
            ),
            Rule(
                rule_id="R54",
                conditions=["slow_heart_rate"],
                disease="typhoid",
                confidence_boost=8,
                severity="medium",
                explanation="Slow heart rate alone is a moderate typhoid indicator."
            ),
            Rule(
                rule_id="R55",
                conditions=["enlarged_liver"],
                disease="typhoid",
                confidence_boost=7,
                severity="medium",
                explanation="Enlarged liver alone is a weak typhoid indicator."
            ),
            Rule(
                rule_id="R56",
                conditions=["constipation"],
                disease="typhoid",
                confidence_boost=5,
                severity="medium",
                explanation="Constipation alone is a weak typhoid indicator."
            ),
            Rule(
                rule_id="R57",
                conditions=["enlarged_spleen"],
                disease="malaria",
                confidence_boost=8,
                severity="high",
                explanation="Enlarged spleen alone is a moderate malaria indicator."
            ),
            Rule(
                rule_id="R58",
                conditions=["anemia"],
                disease="malaria",
                confidence_boost=6,
                severity="medium",
                explanation="Anemia alone is a weak malaria indicator."
            ),
            Rule(
                rule_id="R59",
                conditions=["shivering"],
                disease="malaria",
                confidence_boost=7,
                severity="medium",
                explanation="Shivering/rigors alone is a weak malaria indicator."
            ),
            Rule(
                rule_id="R60",
                conditions=["sore_throat"],
                disease="common_flu",
                confidence_boost=6,
                severity="low",
                explanation="Sore throat alone is a weak flu indicator."
            ),
            Rule(
                rule_id="R61",
                conditions=["runny_nose"],
                disease="common_flu",
                confidence_boost=6,
                severity="low",
                explanation="Runny nose alone is a weak flu indicator."
            ),
            Rule(
                rule_id="R62",
                conditions=["sneezing"],
                disease="common_flu",
                confidence_boost=5,
                severity="low",
                explanation="Sneezing alone is a weak flu indicator."
            ),
            Rule(
                rule_id="R63",
                conditions=["body_ache"],
                disease="common_flu",
                confidence_boost=5,
                severity="low",
                explanation="Body ache alone is a weak flu indicator."
            ),
            Rule(
                rule_id="R64",
                conditions=["cough"],
                disease="common_flu",
                confidence_boost=6,
                severity="low",
                explanation="Cough alone is a weak flu indicator."
            ),
            Rule(
                rule_id="R65",
                conditions=["moderate_fever"],
                disease="common_flu",
                confidence_boost=6,
                severity="low",
                explanation="Mild fever alone is a weak flu indicator."
            ),
            Rule(
                rule_id="R66",
                conditions=["weakness"],
                disease="typhoid",
                confidence_boost=5,
                severity="medium",
                explanation="Weakness alone is a weak typhoid indicator."
            ),
            Rule(
                rule_id="R67",
                conditions=["vomiting"],
                disease="dengue",
                confidence_boost=5,
                severity="medium",
                explanation="Vomiting alone is a weak dengue indicator."
            ),
            Rule(
                rule_id="R68",
                conditions=["nausea"],
                disease="dengue",
                confidence_boost=5,
                severity="medium",
                explanation="Nausea alone is a weak dengue indicator."
            ),
            Rule(
                rule_id="R69",
                conditions=["muscle_pain"],
                disease="malaria",
                confidence_boost=5,
                severity="medium",
                explanation="Muscle pain alone is a weak malaria indicator."
            ),
            Rule(
                rule_id="R70",
                conditions=["fatigue"],
                disease="common_flu",
                confidence_boost=5,
                severity="low",
                explanation="Fatigue alone is a weak flu indicator."
            ),
            Rule(
                rule_id="R71",
                conditions=["headache"],
                disease="typhoid",
                confidence_boost=5,
                severity="low",
                explanation="Headache alone is a weak typhoid indicator."
            ),
            Rule(
                rule_id="R72",
                conditions=["diarrhea"],
                disease="typhoid",
                confidence_boost=6,
                severity="medium",
                explanation="Diarrhea alone is a weak typhoid indicator."
            ),
            Rule(
                rule_id="R73",
                conditions=["moderate_fever", "cough", "sore_throat"],
                disease="common_flu",
                confidence_boost=12,
                severity="low",
                explanation="Moderate fever + cough + sore throat suggests flu or early stage infection."
            ),
            Rule(
                rule_id="R74",
                conditions=["moderate_fever", "headache", "body_ache"],
                disease="common_flu",
                confidence_boost=10,
                severity="low",
                explanation="Moderate fever + headache + body ache is a common flu pattern."
            ),
            Rule(
                rule_id="R75",
                conditions=["moderate_fever", "abdominal_pain"],
                disease="typhoid",
                confidence_boost=8,
                severity="medium",
                explanation="Moderate fever with abdominal pain is a weak typhoid indicator."
            ),
        ]

        for rule in rules:
            self.add_rule(rule)

    def summary(self) -> dict:
        """Returns a summary of rules loaded per disease."""
        summary = {}
        for rule in self.rules:
            summary[rule.disease] = summary.get(rule.disease, 0) + 1
        return summary


# ── Quick test when run directly ─────────────

if __name__ == "__main__":
    kb = KnowledgeBase()
    print("=" * 55)
    print("  MEDICAL EXPERT SYSTEM — Knowledge Base Loaded")
    print("=" * 55)
    summary = kb.summary()
    total = sum(summary.values())
    for disease, count in summary.items():
        print(f"  {disease:<20} → {count} rules")
    print(f"  {'TOTAL':<20} → {total} rules")
    print("=" * 55)

    print("\n📋 Sample rules for DENGUE:\n")
    for rule in kb.get_rules_for_disease("dengue"):
        print(f"  [{rule.rule_id}] IF {rule.conditions}")
        print(f"        THEN → {rule.disease} (+{rule.confidence_boost} confidence)")
        print(f"        WHY  → {rule.explanation}")
        print()
