# 🏥 Medical Expert System
### A Rule-Based Diagnostic Assistant for Fever-Related Diseases

---

## 📌 Project Overview

This project implements a **rule-based expert system** for medical diagnosis
of fever-related diseases. It uses **forward chaining inference** to match
patient symptoms against a medical knowledge base and produce ranked
diagnoses with confidence scores and explanations.

**Diseases Covered:**
- 🤧 Common Flu (Influenza)
- 🦟 Dengue Fever
- 🦟 Malaria
- 🦠 Typhoid Fever

---

## 🎯 Why an Expert System?

Medical diagnosis is one of the most justified domains for expert systems
because:

1. **Structured Knowledge** — Medical guidelines (WHO protocols) can be
   directly encoded as IF-THEN rules from domain experts (doctors).

2. **Consistency** — Unlike human doctors who may vary due to fatigue or
   bias, a rule-based system gives the same output for the same input
   every time.

3. **Accessibility** — In rural or under-resourced areas, an expert system
   serves as a first-line triage tool where specialist doctors aren't
   available.

4. **Explainability** — Rule-based systems can tell the patient WHY a
   diagnosis was made by tracing back through the exact rules that fired.
   This is essential for medical trust and regulatory compliance.

5. **No Training Data Needed** — Unlike ML models, expert systems don't
   need large labeled datasets. Knowledge is encoded directly from medical
   literature.

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────┐
│              USER INTERFACE                     │
│     CLI (rich)  |  Web Dashboard (Streamlit)    │
└──────────────────────┬──────────────────────────┘
                       │ Symptoms Input
┌──────────────────────▼──────────────────────────┐
│              INFERENCE ENGINE                   │
│   Forward Chaining — matches facts to rules     │
│   Confidence Scoring — ranks diseases           │
│   Explanation Module — why this diagnosis?      │
└───────┬──────────────┬──────────────┬───────────┘
        │              │              │
┌───────▼──────┐ ┌─────▼──────┐ ┌────▼──────────┐
│  KNOWLEDGE   │ │  WORKING   │ │  EXPLANATION  │
│    BASE      │ │  MEMORY    │ │    MEMORY     │
│  (40 rules)  │ │ (symptoms) │ │ (fired rules) │
└──────────────┘ └────────────┘ └───────────────┘
```

### Three Core Components:

| Component | File | Purpose |
|---|---|---|
| Knowledge Base | `core/knowledge_base.py` | Stores all 40 IF-THEN rules |
| Working Memory | `core/working_memory.py` | Holds current patient facts |
| Inference Engine | `core/inference_engine.py` | Runs forward chaining logic |
| Explanation Module | `core/explanation.py` | Explains why rules fired |

---

## 🔧 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.10+ | Core implementation |
| Web UI | Streamlit | Interactive web dashboard |
| CLI UI | Rich | Colored terminal interface |
| Testing | Pytest | 44 automated test cases |
| Data | JSON | Disease and symptom definitions |

---

## 📁 Project Structure
```
medical_expert_system/
├── core/
│   ├── __init__.py
│   ├── knowledge_base.py      # Rule class + 40 encoded rules
│   ├── working_memory.py      # Patient fact storage
│   ├── inference_engine.py    # Forward chaining engine
│   └── explanation.py         # Why-explanation module
├── data/
│   └── diseases.json          # Disease metadata + symptom labels
├── ui/
│   ├── cli_app.py             # Terminal interface (rich)
│   └── streamlit_app.py       # Web dashboard (streamlit)
├── tests/
│   └── test_diagnosis.py      # 44 pytest test cases
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Web Dashboard (recommended)
```bash
streamlit run ui/streamlit_app.py
```
Opens at: `http://localhost:8501`

### 3. Run CLI Interface
```bash
python ui/cli_app.py
```

### 4. Run Tests
```bash
python -m pytest tests/test_diagnosis.py -v
```

---

## 🧠 How the Inference Engine Works

The system uses **Forward Chaining**:
```
START with FACTS (patient symptoms)
    ↓
CHECK every Rule in Knowledge Base
    ↓
IF all conditions of a rule match → FIRE the rule
    ↓
Accumulate confidence score per disease
    ↓
Normalize scores to percentages
    ↓
RANK diseases by confidence (highest first)
    ↓
RETURN diagnoses + explanation
```

### Confidence Scoring:

Each rule has a `confidence_boost` value:

| Boost Value | Signal Strength |
|---|---|
| 5  | Weak signal (single symptom) |
| 8–10 | Moderate signal |
| 12–15 | Strong signal |
| 18–20 | Very strong / near-diagnostic |

Multiple rules firing for the same disease accumulate confidence.
Final scores are normalized to sum to 100%.

### Example:

Patient symptoms: `high_fever, severe_headache, pain_behind_eyes, joint_pain, rash`
```
R07 fires → dengue  +20  (high_fever + severe_headache + pain_behind_eyes)
R08 fires → dengue  +20  (high_fever + joint_pain + rash)
R11 fires → dengue  +18  (high_fever + pain_behind_eyes + joint_pain)
R29 fires → dengue  + 5  (high_fever)
R30 fires → malaria + 5  (high_fever)
R31 fires → typhoid + 5  (high_fever)

Total dengue    = 63  → 63/73 = 86.3%
Total malaria   =  5  →  5/73 =  6.8%
Total typhoid   =  5  →  5/73 =  6.8%

Top Diagnosis → Dengue Fever (86.3%)
```

---

## 🧪 Test Results
```
44 tests collected
44 passed, 0 failed

Test Classes:
  TestKnowledgeBase       — 6 tests
  TestWorkingMemory       — 9 tests
  TestCommonFluDiagnosis  — 4 tests
  TestDengueDiagnosis     — 5 tests
  TestMalariaDiagnosis    — 5 tests
  TestTyphoidDiagnosis    — 5 tests
  TestEdgeCases           — 7 tests
  TestExplanationModule   — 3 tests
```

---

## ⚠️ Disclaimer

This system is built for **educational purposes only** as part of an
academic AI project. It is not a substitute for professional medical
advice, diagnosis, or treatment. Always consult a qualified doctor.

---

## 👩‍💻 Project Info

- **Topic:** Rule-Based Expert System for Medical Diagnosis
- **Domain:** Fever-Related Diseases
- **Approach:** Forward Chaining Inference Engine
- **Rules:** 40 IF-THEN rules based on WHO guidelines
- **Tests:** 44 automated test cases
```

---

## How to Check it — Step by Step

**Step 1** — Create the file in your root folder:
```
README.md   ← paste the content above
```

**Step 2** — Your final complete folder structure:
```
medical_expert_system/
├── core/
│   ├── __init__.py          ✅
│   ├── knowledge_base.py    ✅
│   ├── working_memory.py    ✅
│   ├── inference_engine.py  ✅
│   └── explanation.py       ✅
├── data/
│   └── diseases.json        ✅
├── ui/
│   ├── cli_app.py           ✅
│   └── streamlit_app.py     ✅
├── tests/
│   └── test_diagnosis.py    ✅
├── day1_verify.py           ✅
├── day2_verify.py           ✅
├── requirements.txt         ✅
└── README.md                ← NEW ✅