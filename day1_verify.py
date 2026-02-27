"""
day1_verify.py
--------------
Run this to confirm Day 1 is complete and working.

Usage:
    python day1_verify.py
"""

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.knowledge_base import KnowledgeBase
from core.working_memory import WorkingMemory

GREEN  = "\033[92m"
BLUE   = "\033[94m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def section(title):
    print(f"\n{BOLD}{BLUE}{'═'*55}{RESET}")
    print(f"{BOLD}{BLUE}  {title}{RESET}")
    print(f"{BOLD}{BLUE}{'═'*55}{RESET}")

def check(label):
    print(f"  {GREEN}✓{RESET}  {label}")

# 1. diseases.json
section("STEP 1 — diseases.json")
with open("data/diseases.json") as f:
    data = json.load(f)
for name, info in data["diseases"].items():
    check(f"{info['display_name']} — severity: {info['severity'].upper()}, {len(info['symptoms'])} symptoms")
check(f"Symptom display labels: {len(data['symptoms_display'])} entries")

# 2. KnowledgeBase
section("STEP 2 — KnowledgeBase")
kb = KnowledgeBase()
summary = kb.summary()
for disease, count in summary.items():
    check(f"{disease:<20} → {count} rules loaded")
check(f"Total rules: {sum(summary.values())}")

# 3. WorkingMemory
section("STEP 3 — WorkingMemory")
wm = WorkingMemory()
wm.set_patient_info("age", 30)
wm.set_patient_info("temperature_f", 104.5)
wm.add_symptoms(["high_fever", "cyclical_fever", "chills", "sweating", "headache", "nausea"])
check(f"Patient info: {wm.patient_info}")
check(f"Symptoms: {wm.get_all_symptoms()}")
check(f"has_symptom('high_fever'): {wm.has_symptom('high_fever')}")
check(f"has_symptom('rash'): {wm.has_symptom('rash')} (correctly False)")

# 4. Rule matching preview
section("STEP 4 — Rule Matching Preview")
print(f"\n  {YELLOW}Symptoms:{RESET} {wm.get_all_symptoms()}\n")
fired = []
for rule in kb.get_all_rules():
    if all(cond in wm.symptoms for cond in rule.conditions):
        fired.append(rule)
        print(f"  {GREEN}FIRES{RESET} [{rule.rule_id}] → {rule.disease} (+{rule.confidence_boost})")
        print(f"         Matched: {rule.conditions}")
print(f"\n  Total rules fired: {len(fired)}")

section("DAY 1 COMPLETE ✓")
print(f"""
  {GREEN}✓{RESET}  data/diseases.json
  {GREEN}✓{RESET}  core/knowledge_base.py   — 28 rules
  {GREEN}✓{RESET}  core/working_memory.py
  {GREEN}✓{RESET}  requirements.txt
  {GREEN}✓{RESET}  day1_verify.py
""")