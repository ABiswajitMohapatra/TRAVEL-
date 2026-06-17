import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

search_tool = SerperDevTool()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

def get_agents():

    planner = Agent(
        role="Autonomous Travel Planner",
        goal="Create optimal travel plans using real-world constraints",
        backstory="You design realistic itineraries using web data and reasoning.",
        tools=[search_tool],
        llm=llm,
        verbose=True
    )

    critic = Agent(
        role="AI Travel Auditor",
        goal="Detect unrealistic plans and enforce realism",
        backstory="You are strict and remove hallucinated or impossible steps.",
        llm=llm,
        verbose=True
    )

    optimizer = Agent(
        role="Travel Optimization Engine",
        goal="Fix and improve itinerary based on audit feedback",
        backstory="You refine plans into production-grade outputs.",
        llm=llm,
        verbose=True
    )

    return planner, critic, optimizer