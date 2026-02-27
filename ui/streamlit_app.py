"""
streamlit_app.py
----------------
Web dashboard for the Medical Expert System.
Soft White + Blue theme — clean, calm, medical.

Usage:
    streamlit run ui/streamlit_app.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import streamlit as st

from core.knowledge_base import KnowledgeBase
from core.working_memory import WorkingMemory
from core.inference_engine import InferenceEngine
from core.explanation import ExplanationModule


# ── Page Config ──────────────────────────────

st.set_page_config(
    page_title="MedExpert — AI Diagnosis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ── Load Data ────────────────────────────────

@st.cache_resource
def load_kb():
    return KnowledgeBase()

@st.cache_data
def load_disease_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "data", "diseases.json")
    with open(path) as f:
        return json.load(f)


# ── Constants ────────────────────────────────

SEV_COLOR = {
    "low"      : "#34c759",
    "medium"   : "#ff9500",
    "high"     : "#ff3b30",
    "critical" : "#af52de",
}

SEV_BG = {
    "low"      : "#34c75915",
    "medium"   : "#ff950015",
    "high"     : "#ff3b3015",
    "critical" : "#af52de15",
}

SEV_EMOJI = {
    "low"      : "🟢",
    "medium"   : "🟡",
    "high"     : "🔴",
    "critical" : "🟣",
}


# ── CSS ──────────────────────────────────────

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main background — soft white */
    .stApp {
    background: linear-gradient(135deg, #eaf2ff 0%, #f5f0ff 50%, #eafaff 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e0e8f0;
    }

    [data-testid="stSidebar"] * {
        color: #1a2a3a !important;
    }

    /* Input fields */
    input {
        color: #1a2a3a !important;
        background: #f2f6fb !important;
        border: 1px solid #d0dcea !important;
        border-radius: 8px !important;
    }

    input:focus {
        border-color: #0a84ff !important;
        box-shadow: 0 0 0 3px #0a84ff20 !important;
    }

    input::placeholder {
        color: #aabbcc !important;
    }

    [data-testid="stNumberInput"] input {
        color: #1a2a3a !important;
        background: #f2f6fb !important;
    }

    [data-testid="stTextInput"] input {
        color: #1a2a3a !important;
        background: #f2f6fb !important;
    }

    /* Multiselect tags */
    .stMultiSelect [data-baseweb="tag"] {
        background: #e8f0fe !important;
        color: #0a84ff !important;
        border-radius: 6px !important;
    }

    .stMultiSelect [data-baseweb="tag"] span {
        color: #0a84ff !important;
    }

    /* Run diagnosis button */
    .stButton button {
        background: linear-gradient(135deg, #0a84ff, #5e5ce6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.5rem !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 15px #0a84ff30 !important;
        transition: all 0.2s !important;
        margin-bottom: 1rem !important;
    }

    .stButton button:hover {
        box-shadow: 0 6px 20px #0a84ff50 !important;
        transform: translateY(-1px) !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #f2f6fb; }
    ::-webkit-scrollbar-thumb {
        background: #c0d0e0;
        border-radius: 3px;
    }

    /* ── Hero ── */
    .hero {
        background: linear-gradient(135deg, #0a84ff 0%, #5e5ce6 100%);
        border-radius: 20px;
        padding: 2.5rem 3rem;
        text-align: center;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px #0a84ff30;
    }

    .hero::before {
        content: '';
        position: absolute;
        top: -40%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, #ffffff15 0%, transparent 70%);
        pointer-events: none;
    }

    .hero::after {
        content: '';
        position: absolute;
        bottom: -40%;
        left: -5%;
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, #ffffff10 0%, transparent 70%);
        pointer-events: none;
    }

    .hero h1 {
        font-size: 2.6rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.5px;
    }

    .hero p {
        color: #ffffffbb;
        font-size: 0.95rem;
        margin: 0;
        font-weight: 400;
    }

    .badge-row {
        display: flex;
        justify-content: center;
        gap: 0.6rem;
        margin-top: 1.2rem;
        flex-wrap: wrap;
    }

    .badge {
        background: #ffffff20;
        border: 1px solid #ffffff30;
        border-radius: 999px;
        padding: 0.3rem 0.9rem;
        font-size: 0.78rem;
        color: #ffffffdd;
        backdrop-filter: blur(10px);
    }

    /* ── Disclaimer ── */
    .disclaimer {
        background: #fff8e8;
        border: 1px solid #ff950040;
        border-left: 3px solid #ff9500;
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        color: #b86000;
        font-size: 0.83rem;
        margin-bottom: 1.5rem;
    }

    /* ── Section title ── */
    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: #0a84ff;
        margin: 1.5rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        letter-spacing: -0.2px;
    }

    .section-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(to right, #d0dcea, transparent);
        margin-left: 0.5rem;
    }

    /* ── Patient card ── */
    .patient-card {
        background: #ffffff;
        border: 1px solid #e0e8f0;
        border-radius: 14px;
        padding: 1.2rem 1.8rem;
        display: flex;
        gap: 2.5rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 12px #0a84ff08;
        align-items: center;
    }

    .patient-field .p-label {
        font-size: 0.68rem;
        color: #8899aa;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    .patient-field .p-value {
        font-size: 1rem;
        font-weight: 600;
        color: #1a2a3a;
        margin-top: 0.15rem;
    }

    /* ── Top diagnosis card ── */
    .top-card {
        background: #ffffff;
        border: 1px solid #e0e8f0;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px #0a84ff10;
        position: relative;
        overflow: hidden;
    }

    .top-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #0a84ff, #5e5ce6);
    }

    .top-card h2 {
        font-size: 1.9rem;
        font-weight: 700;
        color: #0a84ff;
        margin: 0 0 0.3rem 0;
    }

    .top-card .desc {
        color: #667788;
        font-size: 0.87rem;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }

    .metrics-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 1.2rem;
    }

    .metric-box {
        background: #f2f6fb;
        border: 1px solid #e0e8f0;
        border-radius: 12px;
        padding: 0.9rem 1.3rem;
        min-width: 110px;
        flex: 1;
    }

    .metric-box .m-label {
        font-size: 0.68rem;
        color: #8899aa;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    .metric-box .m-value {
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 0.2rem;
        line-height: 1.2;
    }

    /* ── Confidence bar ── */
    .conf-bar-wrap {
        background: #e8f0fe;
        border-radius: 999px;
        height: 8px;
        width: 100%;
        margin: 1rem 0;
        overflow: hidden;
    }

    .conf-bar-fill {
        height: 100%;
        border-radius: 999px;
    }

    /* ── Action box ── */
    .action-box {
        background: #f0faf4;
        border: 1px solid #34c75930;
        border-left: 3px solid #34c759;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
    }

    .action-label {
        font-size: 0.72rem;
        color: #1a8a3a;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .action-text {
        color: #1a3a2a;
        font-size: 0.88rem;
        line-height: 1.6;
    }

    /* ── Rank cards ── */
    .rank-card {
        background: #ffffff;
        border: 1px solid #e0e8f0;
        border-radius: 12px;
        padding: 1rem 1.3rem;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        box-shadow: 0 1px 6px #0a84ff06;
        transition: box-shadow 0.2s, border-color 0.2s;
    }

    .rank-card:hover {
        box-shadow: 0 4px 16px #0a84ff15;
        border-color: #b0c8e8;
    }

    .rank-num {
        font-size: 1.4rem;
        font-weight: 800;
        color: #d0dcea;
        min-width: 2rem;
        text-align: center;
    }

    .rank-num.top { color: #0a84ff; }

    .rank-info { flex: 1; }

    .rank-name {
        font-weight: 600;
        color: #1a2a3a;
        font-size: 0.93rem;
    }

    .rank-bar-bg {
        background: #e8f0fe;
        border-radius: 999px;
        height: 5px;
        margin-top: 0.4rem;
        overflow: hidden;
    }

    .rank-bar-fill {
        height: 100%;
        border-radius: 999px;
    }

    .rank-conf {
        font-size: 1.1rem;
        font-weight: 700;
        min-width: 55px;
        text-align: right;
    }

    .rank-sev {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        min-width: 72px;
        text-align: center;
        letter-spacing: 0.5px;
    }

    /* ── Rule cards ── */
    .rule-card {
        background: #ffffff;
        border: 1px solid #e0e8f0;
        border-left: 3px solid #0a84ff;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.3rem;
        margin-bottom: 0.7rem;
        box-shadow: 0 1px 6px #0a84ff06;
    }

    .rule-id {
        font-size: 0.72rem;
        font-weight: 700;
        color: #0a84ff;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.35rem;
    }

    .rule-text {
        color: #334455;
        font-size: 0.87rem;
        line-height: 1.55;
        margin-bottom: 0.6rem;
    }

    .rule-meta {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        align-items: center;
    }

    .rule-tag {
        background: #e8f0fe;
        border-radius: 6px;
        padding: 0.18rem 0.55rem;
        font-size: 0.73rem;
        color: #0a84ff;
        font-weight: 500;
    }

    .rule-boost {
        background: #e8fef0;
        border-radius: 6px;
        padding: 0.18rem 0.55rem;
        font-size: 0.73rem;
        color: #1a8a3a;
        font-weight: 600;
    }

    /* ── Welcome cards ── */
    .welcome-card {
        background: #ffffff;
        border: 1px solid #e0e8f0;
        border-radius: 16px;
        padding: 1.8rem 1.5rem;
        text-align: center;
        box-shadow: 0 2px 12px #0a84ff08;
        height: 100%;
    }

    .welcome-card .w-icon {
        font-size: 2.2rem;
        margin-bottom: 0.8rem;
    }

    .welcome-card h4 {
        color: #0a84ff;
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.2px;
    }

    .welcome-card p {
        color: #667788;
        font-size: 0.82rem;
        line-height: 1.6;
        margin: 0;
    }

    /* ── Disease badges ── */
    .disease-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 0.5rem;
    }

    .disease-badge {
        flex: 1;
        min-width: 120px;
        background: #ffffff;
        border: 1px solid #e0e8f0;
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: 0 2px 10px #0a84ff06;
        transition: box-shadow 0.2s;
    }

    .disease-badge:hover {
        box-shadow: 0 4px 18px #0a84ff15;
    }

    .disease-badge .d-icon { font-size: 1.8rem; }

    .disease-badge .d-name {
        font-weight: 600;
        font-size: 0.85rem;
        color: #1a2a3a;
        margin: 0.4rem 0 0.3rem 0;
    }

    .disease-badge .d-sev {
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.18rem 0.6rem;
        border-radius: 999px;
        display: inline-block;
        letter-spacing: 0.5px;
    }

    /* ── Contributing symptoms ── */
    .contrib-box {
        background: #ffffff;
        border: 1px solid #e0e8f0;
        border-radius: 12px;
        padding: 1rem 1.3rem;
        margin-top: 0.5rem;
        box-shadow: 0 1px 6px #0a84ff06;
    }

    .contrib-label {
        font-size: 0.7rem;
        color: #8899aa;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .contrib-tag {
        display: inline-block;
        background: #e8f0fe;
        color: #0a84ff;
        border-radius: 6px;
        padding: 0.2rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.2rem 0.2rem 0.2rem 0;
    }

    /* ── Sidebar logo area ── */
    .sidebar-logo {
        text-align: center;
        padding: 1.2rem 0 1.5rem 0;
        border-bottom: 1px solid #e0e8f0;
        margin-bottom: 1.2rem;
    }

    .sidebar-logo .logo-icon { font-size: 2.2rem; }

    .sidebar-logo .logo-name {
        font-weight: 700;
        font-size: 1.1rem;
        color: #0a84ff;
        margin-top: 0.3rem;
    }

    .sidebar-logo .logo-sub {
        font-size: 0.72rem;
        color: #8899aa;
        margin-top: 0.1rem;
    }

    /* ── No result box ── */
    .no-result {
        background: #fff5f5;
        border: 1px solid #ff3b3030;
        border-left: 3px solid #ff3b30;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        color: #cc2200;
        font-size: 0.88rem;
    }

    /* Symptom count pill */
    .sym-count {
        background: #e8f0fe;
        color: #0a84ff;
        font-size: 0.8rem;
        font-weight: 600;
        border-radius: 999px;
        padding: 0.25rem 0.8rem;
        text-align: center;
        margin-top: 0.5rem;
        display: inline-block;
    }
    
    /* Remove Streamlit anchor icons everywhere */
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }

    </style>
    """, unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────

def render_header():
    st.markdown("""
    <div class="hero">
        <div style="font-size:2.6rem; font-weight:700; color:#ffffff; 
                    letter-spacing:-0.5px; margin-bottom:0.4rem;">
            MedExpert
        </div>
        <p>Rule-Based AI Diagnostic Assistant for Fever-Related Diseases</p>
        <div class="badge-row">
            <span class="badge">🧠 Expert System</span>
            <span class="badge">⚡ Forward Chaining</span>
            <span class="badge">🔍 Explainable AI</span>
            <span class="badge">📊 Confidence Scoring</span>
        </div>
    </div>
    <div class="disclaimer">
        ⚠️ <strong>Disclaimer:</strong>
        This system is for educational purposes only.
        Always consult a qualified medical professional for actual diagnosis and treatment.
    </div>
    """, unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────

def render_sidebar(disease_data: dict):
    st.sidebar.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icon">&#x2695;&#xFE0F;</div>
        <div class="logo-name">MedExpert</div>
        <div class="logo-sub">Diagnostic Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(
        "<p style='font-weight:700; font-size:0.85rem;"
        "color:#1a2a3a; margin-bottom:0.5rem;'>👤 Patient Information</p>",
        unsafe_allow_html=True
    )

    name = st.sidebar.text_input(
        "Name", placeholder="Enter patient name", label_visibility="collapsed"
    )

    col1, col2 = st.sidebar.columns(2)
    with col1:
        age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=25)
    with col2:
        days = st.sidebar.number_input("Days Ill", min_value=1, max_value=30, value=2)

    temp = st.sidebar.number_input(
        "Body Temperature (°F)",
        min_value=95.0, max_value=110.0,
        value=98.6, step=0.1, format="%.1f"
    )

    st.sidebar.markdown("<hr style='border-color:#e0e8f0; margin:1rem 0;'>", unsafe_allow_html=True)

    st.sidebar.markdown(
        "<p style='font-weight:700; font-size:0.85rem;"
        "color:#1a2a3a; margin-bottom:0.3rem;'>🩺 Select Symptoms</p>"
        "<p style='font-size:0.75rem; color:#8899aa; margin-bottom:0.5rem;'>"
        "Select all symptoms the patient is experiencing.</p>",
        unsafe_allow_html=True
    )

    symptom_labels = disease_data["symptoms_display"]
    options = list(symptom_labels.values())

    selected_labels = st.sidebar.multiselect(
        "Symptoms",
        options=options,
        placeholder="🔍 Search symptoms...",
        label_visibility="collapsed"
    )

    count = len(selected_labels)
    if count > 0:
        st.sidebar.markdown(
            f"<div class='sym-count'>✓ {count} symptom(s) selected</div>",
            unsafe_allow_html=True
        )

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    submitted = st.sidebar.button("🔍 Run Diagnosis", use_container_width=True)

    # Build working memory
    wm = WorkingMemory()
    wm.set_patient_info("name", name if name else "Anonymous")
    wm.set_patient_info("age", age)
    wm.set_patient_info("temperature_f", temp)
    wm.set_patient_info("illness_duration_days", days)

    label_to_key = {v: k for k, v in symptom_labels.items()}
    for label in selected_labels:
        key = label_to_key.get(label)
        if key:
            wm.add_symptom(key)

    return wm, submitted, selected_labels


# ── Welcome ──────────────────────────────────

def render_welcome():
    st.markdown("""<div class="section-title">How It Works</div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    cards = [
        ("📋", "Knowledge Base",
         "Contains 76 medical IF-THEN rules based on WHO guidelines covering 4 fever-related diseases."),
        ("⚙️", "Inference Engine",
         "Uses forward chaining to match your symptoms against rules and compute confidence scores."),
        ("💡", "Explanation",
         "Shows exactly which rules fired and why — full transparency into the diagnostic reasoning."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], cards):
        with col:
            st.markdown(f"""
            <div class="welcome-card">
                <div class="w-icon" style="font-style:normal;">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="section-title">Diseases Covered</div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="disease-row">
        <div class="disease-badge">
            <div class="d-icon">🤧</div>
            <div class="d-name">Common Flu</div>
            <div class="d-sev"
                 style="background:#34c75915; color:#34c759;">LOW</div>
        </div>
        <div class="disease-badge">
            <div class="d-icon">🦟</div>
            <div class="d-name">Dengue Fever</div>
            <div class="d-sev"
                 style="background:#ff3b3015; color:#ff3b30;">HIGH</div>
        </div>
        <div class="disease-badge">
            <div class="d-icon">🦟</div>
            <div class="d-name">Malaria</div>
            <div class="d-sev"
                 style="background:#ff3b3015; color:#ff3b30;">HIGH</div>
        </div>
        <div class="disease-badge">
            <div class="d-icon">🦠</div>
            <div class="d-name">Typhoid</div>
            <div class="d-sev"
                 style="background:#ff950015; color:#ff9500;">MEDIUM</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; color:#aabbcc; font-size:0.85rem;
                padding:1.5rem; background:#ffffff; border-radius:14px;
                border:1px solid #e0e8f0;'>
        👈 Fill in patient details and select symptoms from the sidebar,
        then click <strong style="color:#0a84ff;">Run Diagnosis</strong>
    </div>
    """, unsafe_allow_html=True)


# ── Results ──────────────────────────────────

def render_results(results: list, wm: WorkingMemory):
    if not results:
        st.markdown("""
        <div class="no-result">
            ⚠️ <strong>No diagnosis could be made.</strong><br>
            <span style='font-size:0.83rem;'>
            Please select more symptoms and try again.
            </span>
        </div>
        """, unsafe_allow_html=True)
        return

    top = results[0]
    sc  = SEV_COLOR.get(top.severity, "#aaa")
    sb  = SEV_BG.get(top.severity, "#f2f2f2")
    se  = SEV_EMOJI.get(top.severity, "⚪")

    # ── Patient summary ──────────────────────
    st.markdown("""<div class="section-title">👤 Patient Summary</div>""",
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class="patient-card">
        <div class="patient-field">
            <div class="p-label">Name</div>
            <div class="p-value">{wm.get_patient_info('name', 'N/A')}</div>
        </div>
        <div class="patient-field">
            <div class="p-label">Age</div>
            <div class="p-value">{wm.get_patient_info('age', 'N/A')} yrs</div>
        </div>
        <div class="patient-field">
            <div class="p-label">Temperature</div>
            <div class="p-value">{wm.get_patient_info('temperature_f', 'N/A')} °F</div>
        </div>
        <div class="patient-field">
            <div class="p-label">Days Ill</div>
            <div class="p-value">{wm.get_patient_info('illness_duration_days', 'N/A')} day(s)</div>
        </div>
        <div class="patient-field">
            <div class="p-label">Symptoms</div>
            <div class="p-value">{wm.symptom_count()} selected</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Top diagnosis ────────────────────────
    st.markdown("""<div class="section-title">🏆 Top Diagnosis</div>""",
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class="top-card">
        <h2>{top.display_name}</h2>
        <div class="desc">{top.description}</div>
        <div class="metrics-row">
            <div class="metric-box">
                <div class="m-label">Confidence</div>
                <div class="m-value" style="color:#0a84ff;">{top.confidence:.1f}%</div>
            </div>
            <div class="metric-box">
                <div class="m-label">Severity</div>
                <div class="m-value" style="color:{sc};">{se} {top.severity.upper()}</div>
            </div>
            <div class="metric-box">
                <div class="m-label">Rules Fired</div>
                <div class="m-value" style="color:#1a2a3a;">{len(top.fired_rules)}</div>
            </div>
            <div class="metric-box">
                <div class="m-label">Symptoms Matched</div>
                <div class="m-value" style="color:#1a2a3a;">{len(top.matched_symptoms)}</div>
            </div>
        </div>
        <div class="conf-bar-wrap">
            <div class="conf-bar-fill"
                 style="width:{top.confidence}%;
                        background:linear-gradient(90deg, #0a84ff, #5e5ce6);">
            </div>
        </div>
        <div class="action-box">
            <div class="action-label">💊 Recommended Action</div>
            <div class="action-text">{top.recommended_action}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Ranked list ──────────────────────────
    st.markdown("""<div class="section-title">📊 All Diagnoses Ranked</div>""",
                unsafe_allow_html=True)

    for i, r in enumerate(results, 1):
        rc  = SEV_COLOR.get(r.severity, "#aaa")
        rb  = SEV_BG.get(r.severity, "#f2f2f2")
        top_cls = "top" if i == 1 else ""
        st.markdown(f"""
        <div class="rank-card">
            <div class="rank-num {top_cls}">#{i}</div>
            <div class="rank-info">
                <div class="rank-name">{r.display_name}</div>
                <div class="rank-bar-bg">
                    <div class="rank-bar-fill"
                         style="width:{r.confidence}%; background:{rc};">
                    </div>
                </div>
            </div>
            <div class="rank-conf" style="color:{rc};">{r.confidence:.1f}%</div>
            <div class="rank-sev" style="background:{rb}; color:{rc};">
                {r.severity.upper()}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Explanation ──────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="section-title">🔍 Why This Diagnosis?</div>""",
                unsafe_allow_html=True)

    st.markdown(
        f"<p style='color:#667788; font-size:0.86rem; margin-bottom:1rem;'>"
        f"The inference engine fired "
        f"<strong style='color:#0a84ff;'>{len(top.fired_rules)} rule(s)</strong> "
        f"to conclude <strong style='color:#1a2a3a;'>{top.display_name}</strong>.</p>",
        unsafe_allow_html=True
    )

    for rule in top.fired_rules:
        tags_html = "".join(
            f"<span class='rule-tag'>{s}</span>"
            for s in rule.matched_conditions
        )
        st.markdown(f"""
        <div class="rule-card">
            <div class="rule-id">Rule {rule.rule_id}</div>
            <div class="rule-text">{rule.explanation}</div>
            <div class="rule-meta">
                {tags_html}
                <span class="rule-boost">+{rule.confidence_boost} confidence</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Contributing symptoms ────────────────
    if top.matched_symptoms:
        tags = "".join(
            f"<span class='contrib-tag'>{s}</span>"
            for s in top.matched_symptoms
        )
        st.markdown(f"""
        <div class="contrib-box">
            <div class="contrib-label">All Contributing Symptoms</div>
            {tags}
        </div>
        """, unsafe_allow_html=True)


# ── Main ─────────────────────────────────────

def main():
    apply_styles()
    render_header()

    kb           = load_kb()
    disease_data = load_disease_data()

    wm, submitted, selected_labels = render_sidebar(disease_data)

    if not submitted:
        render_welcome()
    else:
        if wm.symptom_count() == 0:
            st.warning("⚠️ Please select at least one symptom before running diagnosis.")
            render_welcome()
        else:
            with st.spinner("🔍 Analyzing symptoms..."):
                engine  = InferenceEngine(kb, wm)
                results = engine.run()
            render_results(results, wm)


if __name__ == "__main__":
    main()