"""Renders the Analytics tab and handles AI-driven data synthesis."""

import streamlit as st
import plotly.express as px
import google.generativeai as genai
from src.database_manager import get_journal_data

def render_analytics_tab() -> None:
    df = get_journal_data()
    
    if not df.empty:
        st.subheader("📈 Emotional Journey")
        df = df.sort_values(by='entry_date')
        
        fig1 = px.line(df, x='entry_date', y='ml_sentiment_score', markers=True, template="plotly_dark")
        fig1.update_yaxes(range=[0, 10], title="Mood Score")
        fig1.update_xaxes(title="Date")
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
        
        st.markdown("---")
        
        colA, colB = st.columns(2)
        with colA:
            st.subheader("🔍 Trigger Frequency")
            trigger_counts = df['trigger_category'].value_counts().reset_index()
            fig2 = px.pie(trigger_counts, values='count', names='trigger_category', hole=0.4, template="plotly_dark")
            st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
            
        with colB:
            st.subheader("⚠️ Trigger Severity")
            severity_df = df.groupby('trigger_category')['ml_sentiment_score'].mean().reset_index()
            severity_df = severity_df.sort_values(by='ml_sentiment_score')
            
            fig3 = px.bar(
                severity_df, 
                x='ml_sentiment_score', 
                y='trigger_category', 
                orientation='h',
                color='ml_sentiment_score', 
                color_continuous_scale="RdYlGn", 
                template="plotly_dark"
            )
            fig3.update_xaxes(range=[0, 10], title="Average Mood Score")
            fig3.update_yaxes(title="")
            st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
            
        st.markdown("---")
        st.subheader("🧠 AI Clinical Synthesis")
        st.caption("Let AntarMitra analyze your raw data to find hidden psychological patterns.")
        
        if st.button("✨ Generate Personalized Trend Report", use_container_width=True):
            with st.spinner("Synthesizing your biometric and emotional data..."):
                try:
                    recent_df = df.head(10) 
                    avg_score = recent_df['ml_sentiment_score'].mean()
                    
                    trigger_means = recent_df.groupby('trigger_category')['ml_sentiment_score'].mean()
                    worst_trigger = trigger_means.idxmin() if not trigger_means.empty else "Not enough data yet"
                    
                    data_context = f"""
                    User's Last 10 Entries Avg Score: {avg_score:.1f}/10
                    Most Damaging Trigger: {worst_trigger}
                    Raw Data Logs:
                    {recent_df[['ml_sentiment_score', 'trigger_category']].to_string(index=False)}
                    """
                    
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"""
                    Act as a high-end AI Behavioral Analyst. 
                    Data: {data_context}
                    Task: Write a highly professional, empathetic, 3-bullet 'Executive Summary' of their mental health trends. 
                    - Point out what their worst trigger is and offer one specific way to mitigate it.
                    - Do not use generic advice. Base it entirely on the numbers provided.
                    """
                    
                    response = model.generate_content(prompt)
                    st.success("### 📊 Your Behavioral Insight Report")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"⚠️ System Error: {e}")
                    
    else:
        st.info("📊 Your analytics dashboard is waiting! Complete your first journal entry to unlock AI insights.")