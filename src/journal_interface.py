"""Renders the Daily Journal tab and handles biometric data capture."""

import streamlit as st
import time
from streamlit_lottie import st_lottie
from src.trigger_analysis import detect_lifestyle_triggers
from src.database_manager import save_journal_entry
from src.ai_coach import generate_ai_motivation

def render_journal_tab(analyzer, lottie_breathing) -> None:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Daily Journal")
        
        if 'start_time' not in st.session_state:
            st.session_state['start_time'] = time.time()
            
        user_input = st.text_area(
            "What's on your mind? (Your data stays local)", 
            placeholder="e.g., I'm feeling overwhelmed...",
            height=250
        ).strip()
        
        current_speed = 0
        if len(user_input) > 0:
            elapsed_time = time.time() - st.session_state['start_time']
            current_speed = (elapsed_time / len(user_input)) * 1000
            st.caption(f"⏱️ Analyzed Typing Rhythm: **{current_speed:.0f} ms** per keystroke")
        else:
            st.session_state['start_time'] = time.time()
            st.caption("⏱️ Sensor armed and ready. Start typing...")
        
        if st.button("🚀 Analyze & Generate Support", use_container_width=True):
            if user_input:
                with st.spinner("AntarMitra is analyzing patterns..."):
                    mood_score = analyzer.calculate_mood_score(user_input)
                    trigger = detect_lifestyle_triggers(user_input)

                    stress_penalty = 0
                    if current_speed > 800:
                        stress_penalty = 1.5
                        mood_score = max(0, mood_score - stress_penalty)
                        st.toast("Biometric Alert: Heavy keystroke latency detected.", icon="🧠")

                    motivation = generate_ai_motivation(user_input, mood_score)
                    save_journal_entry(user_input, mood_score, motivation, trigger)
                    
                    st.session_state['res_score'] = mood_score
                    st.session_state['res_advice'] = motivation
                    st.session_state['res_trigger'] = trigger
                    st.session_state['start_time'] = time.time()
                    
                    if stress_penalty > 0:
                        st.toast("Digital Phenotyping factored into analysis.", icon="⚠️")
                    else:
                        st.toast("Entry securely analyzed and saved!", icon="🔒")
            else:
                st.warning("Please share your thoughts before analyzing.")

    with col2:
        st.subheader("📊 Live Analysis")
        if 'res_score' in st.session_state:
            score = st.session_state['res_score']
            
            if score < 3.5:
                st.error("**High Stress Detected**")
                if lottie_breathing:
                    st_lottie(lottie_breathing, height=180, key="breathing_anim")
                st.info("✋ **Breathe with the circle.** Inhale... Hold... Exhale...")
            
            if score < 4:
                st.metric("Mood Vitality", f"{score}/10", delta="- Critical", delta_color="inverse")
            elif score < 7:
                st.metric("Mood Vitality", f"{score}/10", delta="~ Balanced")
            else:
                st.metric("Mood Vitality", f"{score}/10", delta="+ Thriving")

            st.markdown("---")
            st.markdown("### 💡 AI Clinical Insight")
            st.success(st.session_state['res_advice'])
            st.markdown(f"**Primary Trigger:** `{st.session_state['res_trigger']}`")
        else:
            st.info("Complete a journal entry to see your AI mood analysis and clinical suggestions here.")