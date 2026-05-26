from typing import TypedDict, List

from langgraph.graph import StateGraph, END

from agents.planner import generate_plan
from agents.executor import execute_task
from agents.summarizer import summarize_content


class AgentState(TypedDict):

    task: str
    plan: str
    execution_result: str
    summary: str
    logs: List[str]


# Planner Node
def planner_node(state: AgentState):

    logs = state["logs"]

    logs.append("[Planner] Generating execution plan...")

    plan = generate_plan(state["task"])

    logs.append("[Planner] Plan created successfully.")

    return {
        "plan": plan,
        "logs": logs
    }


# Executor Node
def executor_node(state: AgentState):

    logs = state["logs"]

    logs.append("[Executor] Opening browser...")

    result = execute_task(state["task"])

    logs.append("[Executor] Search completed.")

    return {
        "execution_result": result,
        "logs": logs
    }


# Summarizer Node
def summarizer_node(state: AgentState):

    logs = state["logs"]

    logs.append("[Summarizer] Summarizing content...")

    summary = summarize_content(
        state["execution_result"]
    )

    logs.append("[Summarizer] Summary generated.")

    return {
        "summary": summary,
        "logs": logs
    }


graph = StateGraph(AgentState)

graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("summarizer", summarizer_node)

graph.set_entry_point("planner")

graph.add_edge("planner", "executor")
graph.add_edge("executor", "summarizer")
graph.add_edge("summarizer", END)

workflow = graph.compile()