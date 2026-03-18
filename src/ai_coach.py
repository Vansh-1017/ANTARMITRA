"""Interfaces with the Google Gemini API to generate clinical suggestions."""

import google.generativeai as genai

def generate_ai_motivation(text: str, score: float) -> str:
    """Generates personalized advice based on text and calculated mood score."""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        if score < 4:
            context = "Focus on immediate grounding, breathing, and crisis mitigation."
        elif score < 7:
            context = "Focus on energy management, identifying burnout, and small wins."
        else:
            context = "Focus on gratitude, momentum protection, and high-performance habits."

        prompt = f"""
        Act as AntarMitra, a high-end AI Wellness Coach.
        User Input: "{text}"
        Mood Score: {score}/10
        Strategy: {context}
        
        Task: Provide a brief validation and 3 punchy next steps.
        Format: Use bold bullet points. Keep it under 50 words.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"API Error: {e}")
        if score < 4:
            return "🎯 **Focus:** Calm your nervous system. **Action:** Drink water and sit in silence for 2 mins."
        return "🎯 **Focus:** Maintain your flow. **Action:** Write down one win from today."