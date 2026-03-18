"""
AntarMitra: AI Wellness Companion
Main Application Entry Point
"""

import streamlit as st
import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

from src.database_manager import update_db_schema
from src.local_ai import MoodAnalyzer
from src.journal_interface import render_journal_tab
from src.analytics_dashboard import render_analytics_tab

# --- Application Configuration ---
st.set_page_config(page_title="AntarMitra", page_icon="🧠", layout="wide")

try:
    with open("assets/theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# --- Environment & API Setup ---
load_dotenv() 
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# --- Resource Initialization ---
@st.cache_resource
def initialize_ai_engine():
    """Caches the local ML model to prevent reloading on user interactions."""
    return MoodAnalyzer()

@st.cache_data
def load_lottie_animation(url: str):
    """Fetches Lottie JSON animations safely."""
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

analyzer = initialize_ai_engine()
update_db_schema()
lottie_breathing = load_lottie_animation("https://assets5.lottiefiles.com/packages/lf20_96bovdur.json")

# --- UI Routing ---
st.title("🧠 AntarMitra: AI Wellness Companion")
st.markdown("---")

st.sidebar.subheader("🚀 Project Credits")
st.sidebar.info("**Prepared by:**\n- Vansh Sardana")
st.sidebar.caption("v3.0.0 | Production Architecture")

tab1, tab2 = st.tabs(["📝 Daily Journal", "📊 Mood Analytics"])

with tab1:
    render_journal_tab(analyzer, lottie_breathing)

with tab2:
    render_analytics_tab()