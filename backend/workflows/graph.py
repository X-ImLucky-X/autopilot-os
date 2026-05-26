from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.planner import generate_plan
from agents.executor import execute_task
from agents.summarizer import summarize_content


# State schema
class AgentState(TypedDict):

    task: str
    plan: str
    execution_result: str
    summary: str


# Planner Node
def planner_node(state: AgentState):

    plan = generate_plan(state["task"])

    return {
        "plan": plan
    }


# Executor Node
def executor_node(state: AgentState):

    result = execute_task(state["task"])

    return {
        "execution_result": result
    }


# Summarizer Node
def summarizer_node(state: AgentState):

    summary = summarize_content(
        state["execution_result"]
    )

    return {
        "summary": summary
    }


# Build Graph
graph = StateGraph(AgentState)

graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("summarizer", summarizer_node)

graph.set_entry_point("planner")

graph.add_edge("planner", "executor")
graph.add_edge("executor", "summarizer")
graph.add_edge("summarizer", END)

workflow = graph.compile()