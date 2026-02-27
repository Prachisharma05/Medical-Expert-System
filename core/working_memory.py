"""
working_memory.py
-----------------
Manages the current patient session's facts.
Working Memory is the short-term memory of the expert system —
it holds everything known about the current patient.

Facts include:
  - Symptoms reported (as a set of symptom keys)
  - Patient metadata (age, temperature, illness duration)
"""


class WorkingMemory:
    """
    Holds all facts about the current patient.
    The inference engine reads from this to match against rules.
    """

    def __init__(self):
        self.symptoms: set = set()        # e.g., {"high_fever", "chills", "rash"}
        self.patient_info: dict = {}      # e.g., {"age": 25, "temperature": 103.5}

    # ── Symptom Management ──────────────────────

    def add_symptom(self, symptom: str):
        """Add a single symptom fact."""
        self.symptoms.add(symptom.strip().lower())

    def add_symptoms(self, symptoms: list):
        """Add multiple symptom facts at once."""
        for s in symptoms:
            self.add_symptom(s)

    def remove_symptom(self, symptom: str):
        """Remove a symptom if present."""
        self.symptoms.discard(symptom.strip().lower())

    def has_symptom(self, symptom: str) -> bool:
        """Check if a symptom is present."""
        return symptom.strip().lower() in self.symptoms

    def clear_symptoms(self):
        """Clear all symptoms (start fresh)."""
        self.symptoms.clear()

    # ── Patient Info ─────────────────────────────

    def set_patient_info(self, key: str, value):
        """Store a patient metadata field."""
        self.patient_info[key] = value

    def get_patient_info(self, key: str, default=None):
        """Retrieve a patient metadata field."""
        return self.patient_info.get(key, default)

    # ── Utility ──────────────────────────────────

    def reset(self):
        """Fully reset working memory for a new patient."""
        self.symptoms.clear()
        self.patient_info.clear()

    def get_all_symptoms(self) -> list:
        """Return sorted list of all current symptoms."""
        return sorted(list(self.symptoms))

    def symptom_count(self) -> int:
        return len(self.symptoms)

    def __repr__(self):
        return (
            f"WorkingMemory(\n"
            f"  symptoms={self.get_all_symptoms()},\n"
            f"  patient_info={self.patient_info}\n"
            f")"
        )


# ── Quick test when run directly ─────────────

if __name__ == "__main__":
    wm = WorkingMemory()

    wm.set_patient_info("name", "Test Patient")
    wm.set_patient_info("age", 28)
    wm.set_patient_info("temperature_f", 104.2)
    wm.set_patient_info("illness_duration_days", 4)

    wm.add_symptoms(["high_fever", "chills", "sweating", "cyclical_fever", "headache"])

    print(wm)
    print(f"\nHas 'high_fever'? {wm.has_symptom('high_fever')}")
    print(f"Has 'rash'?       {wm.has_symptom('rash')}")
    print(f"Total symptoms:   {wm.symptom_count()}")