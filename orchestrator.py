from crewai import Task, Crew, Process
from agents import get_agents


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
            agent=planner,
            expected_output="A detailed day-by-day travel itinerary with activities, costs, and logistics."
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
            context=[plan_task],
            expected_output="A list of issues found in the travel plan regarding cost, time, and logistics."
        )

        optimize_task = Task(
            description="""
Fix issues and produce final improved itinerary.
Return only corrected version.
""",
            agent=optimizer,
            context=[plan_task, critique_task],
            expected_output="A corrected, production-ready travel itinerary addressing all identified issues."
        )

        crew = Crew(
            agents=[planner, critic, optimizer],
            tasks=[plan_task, critique_task, optimize_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()

        if result and len(str(result)) > 200:
            final_output = result
            break

    return final_output
