import streamlit as st
import pandas as pd
import os
import json

st.set_page_config(page_title="NetSage-AI Dashboard", page_icon="📡", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }
    .main-title {
        font-size: 3rem;
        color: #00D2FF;
        font-weight: 700;
        margin-bottom: 0rem;
        animation: fadeIn 0.8s ease-out forwards;
    }
    .main-title span {
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #A0AEC0;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out forwards;
        opacity: 0;
        animation-fill-mode: forwards;
    }
    .metric-card {
        background-color: #1E2130;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
        border-left: 4px solid #00D2FF;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-left-color 0.3s ease;
        animation: fadeIn 1.2s ease-out forwards;
        opacity: 0;
        animation-fill-mode: forwards;
    }
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 210, 255, 0.25);
        border-left-color: #FF007F;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FAFAFA;
    }
    .metric-label {
        font-size: 1rem;
        color: #A0AEC0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        animation: fadeIn 1.5s ease-out forwards;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">NetSage-AI Dashboard <span>📡</span></p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Assisted Network Troubleshooting with Human Review</p>', unsafe_allow_html=True)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
AI_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ai")
REVIEW_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "review")

st.sidebar.markdown("### 🧭 Navigation")
page = st.sidebar.radio("Navigation", ["📊 Overview", "📁 Dataset", "🤖 AI Results", "🧑‍⚖️ Review Logs"], label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.info("NetSage-AI enforces human-in-the-loop review for all AI diagnoses.")

def load_cases():
    path = os.path.join(DATA_DIR, "cases.csv")
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except pd.errors.EmptyDataError:
            pass
    return pd.DataFrame()

def load_ai_results():
    path = os.path.join(AI_DIR, "ai_results.json")
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return pd.DataFrame(json.load(f))
        except json.JSONDecodeError:
            pass
    return pd.DataFrame()

def load_review_logs():
    path = os.path.join(REVIEW_DIR, "review_log.csv")
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except pd.errors.EmptyDataError:
            pass
    return pd.DataFrame()

cases_df = load_cases()
results_df = load_ai_results()
logs_df = load_review_logs()

if page == "📊 Overview":
    st.markdown("### 📈 System Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(cases_df)}</div><div class="metric-label">Total Test Cases</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(results_df)}</div><div class="metric-label">AI Diagnoses Run</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(logs_df)}</div><div class="metric-label">Human Reviews</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not logs_df.empty:
        st.markdown("#### ⚖️ Human Review Decisions")
        decision_counts = logs_df["human_decision"].value_counts()
        st.bar_chart(decision_counts, color="#00D2FF")

elif page == "📁 Dataset":
    st.markdown("### 🗃️ Test Cases Dataset")
    if cases_df.empty:
        st.warning("cases.csv not found or empty.")
    else:
        st.dataframe(cases_df, width="stretch", height=300)
        st.markdown("<br>#### 📉 Fault Categories Distribution", unsafe_allow_html=True)
        st.bar_chart(cases_df["concept_tag"].value_counts(), color="#FF4B4B")

elif page == "🤖 AI Results":
    st.markdown("### 🧠 AI Diagnoses Results")
    if results_df.empty:
        st.info("No AI results found. Run `python ai/diagnose.py` first.")
    else:
        # Reorder columns for better readability if they exist
        cols = results_df.columns.tolist()
        if "case_id" in cols:
            cols.insert(0, cols.pop(cols.index("case_id")))
        st.dataframe(results_df[cols], width="stretch")

elif page == "🧑‍⚖️ Review Logs":
    st.markdown("### 📝 Human Review Audit Log")
    if logs_df.empty:
        st.info("No review logs found. Run `python review/review_cli.py` first.")
    else:
        st.dataframe(logs_df, width="stretch")
        
        st.markdown("---")
        st.markdown("#### 🚨 Rejected Cases Analysis")
        rejected = logs_df[logs_df["human_decision"] == "Rejected"]
        if rejected.empty:
            st.success("🎉 No rejected cases! All AI diagnoses were accepted.")
        else:
            st.dataframe(rejected[["case_id", "ai_diagnosis", "ai_confidence", "comments"]], width="stretch")
