import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


def call_groq(system_prompt: str, user_prompt: str) -> str:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Add it in Streamlit Cloud → Settings → Secrets.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    response = requests.post(GROQ_URL, headers=headers, json=payload)
    if not response.ok:
        raise Exception(f"Groq API error {response.status_code}: {response.text}")
    return response.json()["choices"][0]["message"]["content"]


def planner_agent(destination, days, budget, interests) -> str:
    system = "You are an expert travel planner. Create realistic, detailed travel itineraries."
    user = f"""
Create a detailed travel plan:
- Destination: {destination}
- Days: {days}
- Budget: ${budget}
- Interests: {interests}

Provide a day-by-day itinerary with morning, afternoon, and evening activities.
Include estimated costs, transport, and accommodation tips.
Be realistic and specific.
"""
    return call_groq(system, user)


def critic_agent(plan: str) -> str:
    system = "You are a strict travel plan auditor. Identify only real problems."
    user = f"""
Review this travel plan and list ONLY genuine issues:
- Unrealistic costs
- Impossible travel times
- Logical inconsistencies
- Budget overruns

Plan:
{plan}

Return a numbered list of issues only. If no issues, say 'No major issues found.'
"""
    return call_groq(system, user)


def optimizer_agent(plan: str, critique: str) -> str:
    system = "You are a travel optimization expert. Fix plans based on audit feedback."
    user = f"""
Original Plan:
{plan}

Issues Found:
{critique}

Produce a corrected, final travel itinerary fixing all issues above.
Format clearly with Day 1, Day 2, etc. Include morning/afternoon/evening for each day.
"""
    return call_groq(system, user)
