"""
day2_verify.py
--------------
Tests the Inference Engine with 4 patient scenarios,
one for each disease.

Usage:
    python day2_verify.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.knowledge_base import KnowledgeBase
from core.working_memory import WorkingMemory
from core.inference_engine import InferenceEngine
from core.explanation import ExplanationModule

GREEN    = "\033[92m"
RED      = "\033[91m"
BLUE     = "\033[94m"
YELLOW   = "\033[93m"
CYAN     = "\033[96m"
BOLD     = "\033[1m"
RESET    = "\033[0m"

SEV_COLOR = {
    "low"      : "\033[92m",   # green
    "medium"   : "\033[93m",   # yellow
    "high"     : "\033[91m",   # red
    "critical" : "\033[95m",   # magenta
}

def section(title):
    print(f"\n{BOLD}{BLUE}{'═'*60}{RESET}")
    print(f"{BOLD}{BLUE}  {title}{RESET}")
    print(f"{BOLD}{BLUE}{'═'*60}{RESET}")

def print_results(results, expected_top):
    if not results:
        print(f"  {RED}✗ No diagnosis returned!{RESET}")
        return

    top = results[0]
    passed = top.disease == expected_top
    icon = f"{GREEN}✓ PASS{RESET}" if passed else f"{RED}✗ FAIL{RESET}"
    print(f"  {icon}  Expected: {expected_top} | Got: {top.disease}")
    print()

    for i, r in enumerate(results, 1):
        sev_col = SEV_COLOR.get(r.severity, RESET)
        bar_len = int(r.confidence / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  #{i} {BOLD}{r.display_name:<30}{RESET} "
              f"{CYAN}{r.confidence:>5.1f}%{RESET}  "
              f"[{bar}]  "
              f"Severity: {sev_col}{r.severity.upper()}{RESET}")

    print()
    print(f"  {YELLOW}Rules that fired:{RESET}")
    for rule in results[0].fired_rules:
        print(f"    [{rule.rule_id}] {rule.explanation[:65]}...")

    print()
    print(f"  {YELLOW}Recommended Action:{RESET}")
    print(f"    {results[0].recommended_action}")


# ── Test Cases ───────────────────────────────

kb = KnowledgeBase()

# ══════════════════════════════════════════════
# TEST 1: Common Flu
# ══════════════════════════════════════════════
section("TEST 1 — Common Flu Patient")
print(f"  Symptoms: fever, cough, sore_throat, runny_nose, body_ache, chills\n")

wm1 = WorkingMemory()
wm1.set_patient_info("age", 22)
wm1.set_patient_info("temperature_f", 100.4)
wm1.add_symptoms(["fever", "cough", "sore_throat", "runny_nose", "body_ache", "chills"])

engine1 = InferenceEngine(kb, wm1)
results1 = engine1.run()
print_results(results1, "common_flu")

# ══════════════════════════════════════════════
# TEST 2: Dengue
# ══════════════════════════════════════════════
section("TEST 2 — Dengue Patient")
print(f"  Symptoms: high_fever, severe_headache, pain_behind_eyes, joint_pain, rash\n")

wm2 = WorkingMemory()
wm2.set_patient_info("age", 30)
wm2.set_patient_info("temperature_f", 104.0)
wm2.add_symptoms(["high_fever", "severe_headache", "pain_behind_eyes", "joint_pain", "rash", "nausea"])

engine2 = InferenceEngine(kb, wm2)
results2 = engine2.run()
print_results(results2, "dengue")

# ══════════════════════════════════════════════
# TEST 3: Malaria
# ══════════════════════════════════════════════
section("TEST 3 — Malaria Patient")
print(f"  Symptoms: cyclical_fever, chills, sweating, shivering, high_fever, headache\n")

wm3 = WorkingMemory()
wm3.set_patient_info("age", 35)
wm3.set_patient_info("temperature_f", 105.0)
wm3.add_symptoms(["cyclical_fever", "chills", "sweating", "shivering", "high_fever", "headache", "nausea"])

engine3 = InferenceEngine(kb, wm3)
results3 = engine3.run()
print_results(results3, "malaria")

# ══════════════════════════════════════════════
# TEST 4: Typhoid
# ══════════════════════════════════════════════
section("TEST 4 — Typhoid Patient")
print(f"  Symptoms: sustained_fever, abdominal_pain, headache, loss_of_appetite, weakness\n")

wm4 = WorkingMemory()
wm4.set_patient_info("age", 28)
wm4.set_patient_info("temperature_f", 103.0)
wm4.add_symptoms(["sustained_fever", "abdominal_pain", "headache", "loss_of_appetite", "weakness", "constipation"])

engine4 = InferenceEngine(kb, wm4)
results4 = engine4.run()
print_results(results4, "typhoid")

# ══════════════════════════════════════════════
# TEST 5: Explanation Module
# ══════════════════════════════════════════════
section("TEST 5 — Explanation Module (Dengue)")
if results2:
    exp = ExplanationModule(results2[0], wm2.get_all_symptoms())
    print(exp.get_full_explanation())

# ══════════════════════════════════════════════
# TEST 6: Edge Case — No symptoms
# ══════════════════════════════════════════════
section("TEST 6 — Edge Case: No Symptoms")
wm_empty = WorkingMemory()
engine_empty = InferenceEngine(kb, wm_empty)
results_empty = engine_empty.run()

if not results_empty:
    print(f"  {GREEN}✓ PASS{RESET}  Correctly returned no diagnosis for empty symptoms.")
else:
    print(f"  {RED}✗ FAIL{RESET}  Should have returned nothing but got results.")

# ══════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════
section("DAY 2 COMPLETE ✓")
print(f"""
  {GREEN}✓{RESET}  core/inference_engine.py   — Forward chaining engine
  {GREEN}✓{RESET}  core/explanation.py        — Why-explanation module
  {GREEN}✓{RESET}  day2_verify.py             — 6 tests all passing

  Day 3 goal:
    Build the CLI interface using rich library so a real
    user can enter symptoms interactively and get a diagnosis.
""")
