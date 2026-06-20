import streamlit as st
import os
from dotenv import load_dotenv
from orchestrator import run_agentic_system

load_dotenv()

st.set_page_config(page_title="Production Agentic AI", layout="wide")
st.title("🧠 Production-Grade Agentic Travel System")

with st.sidebar:
    destination = st.text_input("Destination", "Tokyo")
    days = st.slider("Days", 1, 15, 5)
    budget = st.number_input("Budget ($)", 500, 20000, 3000)
    interests = st.text_input("Interests", "food, culture, tech")
    run = st.button("🚀 Run Agentic System")

if run:
    if not os.getenv("GROQ_API_KEY"):
        st.error("❌ GROQ_API_KEY missing. Go to Streamlit Cloud → App Settings → Secrets and add:\nGROQ_API_KEY = 'your_key_here'")
    else:
        try:
            with st.spinner("🤖 Agents working..."):
                plan, critique, final = run_agentic_system(destination, days, budget, interests)

            st.subheader("📋 Initial Plan")
            st.write(plan)

            st.subheader("🔍 Audit / Critique")
            st.write(critique)

            st.subheader("✅ Final Optimized Itinerary")
            st.write(final)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
