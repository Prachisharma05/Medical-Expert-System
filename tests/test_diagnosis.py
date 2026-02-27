"""
test_diagnosis.py
-----------------
Automated tests for the Medical Expert System.
Tests cover all 4 diseases, edge cases, and the explanation module.

Usage:
    pytest tests/test_diagnosis.py -v
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from core.knowledge_base import KnowledgeBase
from core.working_memory import WorkingMemory
from core.inference_engine import InferenceEngine
from core.explanation import ExplanationModule


# ── Shared fixture ───────────────────────────

@pytest.fixture
def kb():
    """Shared KnowledgeBase instance for all tests."""
    return KnowledgeBase()


def run_diagnosis(kb, symptoms: list) -> list:
    """Helper — create WM, add symptoms, run engine, return results."""
    wm = WorkingMemory()
    wm.add_symptoms(symptoms)
    engine = InferenceEngine(kb, wm)
    return engine.run()


# ══════════════════════════════════════════════
# KNOWLEDGE BASE TESTS
# ══════════════════════════════════════════════

class TestKnowledgeBase:

    def test_rules_loaded(self, kb):
        """Knowledge base should load rules."""
        assert len(kb.get_all_rules()) > 0

    def test_minimum_rule_count(self, kb):
        """Should have at least 28 rules."""
        assert len(kb.get_all_rules()) >= 28

    def test_all_four_diseases_have_rules(self, kb):
        """All 4 diseases must have at least one rule."""
        diseases = set(r.disease for r in kb.get_all_rules())
        assert "common_flu" in diseases
        assert "dengue"     in diseases
        assert "malaria"    in diseases
        assert "typhoid"    in diseases

    def test_rules_have_required_fields(self, kb):
        """Every rule must have all required fields filled."""
        for rule in kb.get_all_rules():
            assert rule.rule_id        != ""
            assert len(rule.conditions) > 0
            assert rule.disease        != ""
            assert rule.confidence_boost > 0
            assert rule.severity       in ["low", "medium", "high", "critical"]
            assert rule.explanation    != ""

    def test_get_rules_for_disease(self, kb):
        """get_rules_for_disease should filter correctly."""
        flu_rules = kb.get_rules_for_disease("common_flu")
        assert all(r.disease == "common_flu" for r in flu_rules)
        assert len(flu_rules) > 0

    def test_rule_ids_are_unique(self, kb):
        """All rule IDs must be unique."""
        ids = [r.rule_id for r in kb.get_all_rules()]
        assert len(ids) == len(set(ids))


# ══════════════════════════════════════════════
# WORKING MEMORY TESTS
# ══════════════════════════════════════════════

class TestWorkingMemory:

    def test_add_single_symptom(self):
        wm = WorkingMemory()
        wm.add_symptom("fever")
        assert wm.has_symptom("fever")

    def test_add_multiple_symptoms(self):
        wm = WorkingMemory()
        wm.add_symptoms(["fever", "cough", "headache"])
        assert wm.symptom_count() == 3

    def test_remove_symptom(self):
        wm = WorkingMemory()
        wm.add_symptom("fever")
        wm.remove_symptom("fever")
        assert not wm.has_symptom("fever")

    def test_clear_symptoms(self):
        wm = WorkingMemory()
        wm.add_symptoms(["fever", "cough", "rash"])
        wm.clear_symptoms()
        assert wm.symptom_count() == 0

    def test_patient_info(self):
        wm = WorkingMemory()
        wm.set_patient_info("age", 25)
        assert wm.get_patient_info("age") == 25

    def test_missing_patient_info_returns_default(self):
        wm = WorkingMemory()
        assert wm.get_patient_info("age", default=0) == 0

    def test_reset(self):
        wm = WorkingMemory()
        wm.add_symptoms(["fever", "cough"])
        wm.set_patient_info("age", 30)
        wm.reset()
        assert wm.symptom_count() == 0
        assert wm.patient_info == {}

    def test_duplicate_symptoms_not_added_twice(self):
        wm = WorkingMemory()
        wm.add_symptom("fever")
        wm.add_symptom("fever")
        assert wm.symptom_count() == 1

    def test_symptom_case_insensitive(self):
        wm = WorkingMemory()
        wm.add_symptom("FEVER")
        assert wm.has_symptom("fever")


# ══════════════════════════════════════════════
# INFERENCE ENGINE — DISEASE TESTS
# ══════════════════════════════════════════════

class TestCommonFluDiagnosis:

    def test_classic_flu_symptoms(self, kb):
        """Classic flu symptoms should diagnose common_flu as top result."""
        results = run_diagnosis(kb, [
            "fever", "cough", "sore_throat",
            "runny_nose", "body_ache", "chills"
        ])
        assert len(results) > 0
        assert results[0].disease == "common_flu"

    def test_flu_confidence_above_threshold(self, kb):
        """Flu diagnosis should have confidence above 30%."""
        results = run_diagnosis(kb, [
            "fever", "cough", "sore_throat", "runny_nose", "sneezing"
        ])
        flu = next((r for r in results if r.disease == "common_flu"), None)
        assert flu is not None
        assert flu.confidence > 30

    def test_flu_severity_is_low(self, kb):
        """Flu should have low severity."""
        results = run_diagnosis(kb, ["fever", "cough", "sore_throat"])
        flu = next((r for r in results if r.disease == "common_flu"), None)
        assert flu is not None
        assert flu.severity == "low"

    def test_flu_has_recommendation(self, kb):
        """Flu result should have a non-empty recommendation."""
        results = run_diagnosis(kb, ["fever", "cough", "sore_throat"])
        flu = next((r for r in results if r.disease == "common_flu"), None)
        assert flu is not None
        assert flu.recommended_action != ""


class TestDengueDiagnosis:

    def test_classic_dengue_symptoms(self, kb):
        """Classic dengue symptoms should diagnose dengue as top result."""
        results = run_diagnosis(kb, [
            "high_fever", "severe_headache", "pain_behind_eyes",
            "joint_pain", "rash", "nausea"
        ])
        assert len(results) > 0
        assert results[0].disease == "dengue"

    def test_dengue_confidence_above_threshold(self, kb):
        """Dengue diagnosis should have confidence above 40%."""
        results = run_diagnosis(kb, [
            "high_fever", "severe_headache",
            "pain_behind_eyes", "joint_pain", "rash"
        ])
        dengue = next((r for r in results if r.disease == "dengue"), None)
        assert dengue is not None
        assert dengue.confidence > 40

    def test_dengue_severity_is_high(self, kb):
        """Dengue should have high severity."""
        results = run_diagnosis(kb, [
            "high_fever", "severe_headache", "pain_behind_eyes"
        ])
        dengue = next((r for r in results if r.disease == "dengue"), None)
        assert dengue is not None
        assert dengue.severity == "high"

    def test_dengue_breakbone_fever(self, kb):
        """Breakbone fever symptoms (joint+muscle pain+rash) should fire."""
        results = run_diagnosis(kb, [
            "high_fever", "joint_pain", "muscle_pain", "rash"
        ])
        dengue = next((r for r in results if r.disease == "dengue"), None)
        assert dengue is not None

    def test_dengue_bleeding_signs(self, kb):
        """Bleeding signs with low platelet should strongly indicate dengue."""
        results = run_diagnosis(kb, [
            "high_fever", "low_platelet", "mild_bleeding"
        ])
        dengue = next((r for r in results if r.disease == "dengue"), None)
        assert dengue is not None
        assert dengue.confidence > 50


class TestMalariaDiagnosis:

    def test_classic_malaria_symptoms(self, kb):
        """Classic malaria symptoms should diagnose malaria as top result."""
        results = run_diagnosis(kb, [
            "cyclical_fever", "chills", "sweating",
            "shivering", "high_fever", "headache"
        ])
        assert len(results) > 0
        assert results[0].disease == "malaria"

    def test_malaria_confidence_above_threshold(self, kb):
        """Malaria diagnosis should have confidence above 40%."""
        results = run_diagnosis(kb, [
            "cyclical_fever", "chills", "sweating", "high_fever"
        ])
        malaria = next((r for r in results if r.disease == "malaria"), None)
        assert malaria is not None
        assert malaria.confidence > 40

    def test_malaria_severity_is_high(self, kb):
        """Malaria should have high severity."""
        results = run_diagnosis(kb, [
            "cyclical_fever", "chills", "sweating"
        ])
        malaria = next((r for r in results if r.disease == "malaria"), None)
        assert malaria is not None
        assert malaria.severity == "high"

    def test_malaria_cyclical_fever_pattern(self, kb):
        """Cyclical fever + chills + sweating is pathognomonic for malaria."""
        results = run_diagnosis(kb, [
            "cyclical_fever", "chills", "sweating"
        ])
        malaria = next((r for r in results if r.disease == "malaria"), None)
        assert malaria is not None

    def test_malaria_splenomegaly(self, kb):
        """Enlarged spleen with fever should indicate malaria."""
        results = run_diagnosis(kb, [
            "enlarged_spleen", "high_fever", "fatigue"
        ])
        malaria = next((r for r in results if r.disease == "malaria"), None)
        assert malaria is not None


class TestTyphoidDiagnosis:

    def test_classic_typhoid_symptoms(self, kb):
        """Classic typhoid symptoms should diagnose typhoid as top result."""
        results = run_diagnosis(kb, [
            "sustained_fever", "abdominal_pain", "headache",
            "loss_of_appetite", "weakness", "constipation"
        ])
        assert len(results) > 0
        assert results[0].disease == "typhoid"

    def test_typhoid_confidence_above_threshold(self, kb):
        """Typhoid diagnosis should have confidence above 40%."""
        results = run_diagnosis(kb, [
            "sustained_fever", "headache",
            "abdominal_pain", "loss_of_appetite"
        ])
        typhoid = next((r for r in results if r.disease == "typhoid"), None)
        assert typhoid is not None
        assert typhoid.confidence > 40

    def test_typhoid_rose_spots(self, kb):
        """Rose spots with sustained fever is nearly diagnostic for typhoid."""
        results = run_diagnosis(kb, [
            "rose_spots", "sustained_fever", "headache"
        ])
        typhoid = next((r for r in results if r.disease == "typhoid"), None)
        assert typhoid is not None
        assert typhoid.confidence > 50

    def test_typhoid_bradycardia(self, kb):
        """Slow heart rate with sustained fever should indicate typhoid."""
        results = run_diagnosis(kb, [
            "slow_heart_rate", "sustained_fever"
        ])
        typhoid = next((r for r in results if r.disease == "typhoid"), None)
        assert typhoid is not None

    def test_typhoid_severity_is_medium(self, kb):
        """Typhoid should have medium severity."""
        results = run_diagnosis(kb, [
            "sustained_fever", "abdominal_pain", "headache"
        ])
        typhoid = next((r for r in results if r.disease == "typhoid"), None)
        assert typhoid is not None
        assert typhoid.severity == "medium"


# ══════════════════════════════════════════════
# EDGE CASE TESTS
# ══════════════════════════════════════════════

class TestEdgeCases:

    def test_no_symptoms_returns_empty(self, kb):
        """Empty symptoms should return no diagnosis."""
        results = run_diagnosis(kb, [])
        assert results == []

    def test_single_symptom_returns_result(self, kb):
        """A single symptom should still return some result."""
        results = run_diagnosis(kb, ["high_fever"])
        assert len(results) > 0

    def test_results_sorted_by_confidence(self, kb):
        """Results must always be sorted highest confidence first."""
        results = run_diagnosis(kb, [
            "high_fever", "chills", "sweating",
            "cyclical_fever", "headache"
        ])
        for i in range(len(results) - 1):
            assert results[i].confidence >= results[i + 1].confidence

    def test_confidence_adds_to_100(self, kb):
        """All confidence percentages must add up to ~100%."""
        results = run_diagnosis(kb, [
            "high_fever", "severe_headache", "pain_behind_eyes",
            "joint_pain", "rash"
        ])
        total = sum(r.confidence for r in results)
        assert abs(total - 100.0) < 1.0  # allow tiny floating point error

    def test_unrelated_symptoms_still_work(self, kb):
        """Unknown/irrelevant symptom keys should not crash the system."""
        results = run_diagnosis(kb, ["fever", "unknown_symptom_xyz"])
        # Should still work, just ignoring the unknown one
        assert isinstance(results, list)

    def test_all_results_have_display_name(self, kb):
        """Every result must have a non-empty display name."""
        results = run_diagnosis(kb, [
            "high_fever", "cough", "chills"
        ])
        for r in results:
            assert r.display_name != ""

    def test_all_results_have_recommendation(self, kb):
        """Every result must have a recommendation."""
        results = run_diagnosis(kb, [
            "high_fever", "cough", "chills"
        ])
        for r in results:
            assert r.recommended_action != ""


# ══════════════════════════════════════════════
# EXPLANATION MODULE TESTS
# ══════════════════════════════════════════════

class TestExplanationModule:

    def test_full_explanation_not_empty(self, kb):
        """Full explanation should return a non-empty string."""
        results = run_diagnosis(kb, [
            "high_fever", "severe_headache", "pain_behind_eyes"
        ])
        assert len(results) > 0
        exp = ExplanationModule(results[0], ["high_fever", "severe_headache", "pain_behind_eyes"])
        text = exp.get_full_explanation()
        assert len(text) > 0

    def test_full_explanation_contains_disease(self, kb):
        """Full explanation should mention the disease name."""
        results = run_diagnosis(kb, [
            "cyclical_fever", "chills", "sweating"
        ])
        assert len(results) > 0
        exp = ExplanationModule(results[0], ["cyclical_fever", "chills", "sweating"])
        text = exp.get_full_explanation()
        assert results[0].display_name in text

    def test_short_explanation_not_empty(self, kb):
        """Short explanation should return a non-empty string."""
        results = run_diagnosis(kb, [
            "sustained_fever", "abdominal_pain", "headache"
        ])
        assert len(results) > 0
        exp = ExplanationModule(results[0], ["sustained_fever", "abdominal_pain", "headache"])
        text = exp.get_short_explanation()
        assert len(text) > 0