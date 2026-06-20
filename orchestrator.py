from agents import planner_agent, critic_agent, optimizer_agent


def run_agentic_system(destination, days, budget, interests):
    plan = planner_agent(destination, days, budget, interests)
    critique = critic_agent(plan)
    final = optimizer_agent(plan, critique)
    return plan, critique, final
