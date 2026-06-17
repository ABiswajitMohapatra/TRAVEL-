from crewai import Task, Crew, Process
from agents import get_agents
from schemas import TravelPlan

def run_agentic_system(destination, days, budget, interests):

    planner, critic, optimizer = get_agents()

    max_iterations = 2
    final_output = None

    for i in range(max_iterations):

        plan_task = Task(
            description=f"""
Create travel plan:

Destination: {destination}
Days: {days}
Budget: {budget}
Interests: {interests}

Must be realistic and structured.
""",
            agent=planner
        )

        critique_task = Task(
            description="""
Critically evaluate the plan:
- cost realism
- time feasibility
- travel distance logic

Return issues only.
""",
            agent=critic,
            context=[plan_task]
        )

        optimize_task = Task(
            description="""
Fix issues and produce final improved itinerary.
Return only corrected version.
""",
            agent=optimizer,
            context=[plan_task, critique_task]
        )

        crew = Crew(
            agents=[planner, critic, optimizer],
            tasks=[plan_task, critique_task, optimize_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()

        # production safety check (basic gate)
        if result and len(str(result)) > 200:
            final_output = result
            break

    return final_output