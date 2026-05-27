from typing import TypedDict, List
from datetime import datetime, timedelta

from langgraph.graph import StateGraph, END

from agents.planner import generate_plan
from agents.executor import execute_task
from agents.summarizer import summarize_content
from agents.email_agent import email_summary
from agents.calendar_agent import extract_calendar_details

from tools.calendar_tool import create_calendar_event


class AgentState(TypedDict):

    # Core task
    task: str

    # Tool routing
    tool_decision: str

    # Email
    email_requested: bool
    recipient: str

    # Calendar
    calendar_requested: bool
    calendar_details: dict

    # Workflow outputs
    plan: str
    execution_result: str
    summary: str

    # Logs
    logs: List[str]


# ---------------------------
# Planner Node
# ---------------------------

def planner_node(state: AgentState):

    logs = state["logs"]

    logs.append(
        "[Planner] Generating execution plan..."
    )

    plan = generate_plan(
        state["task"]
    )

    logs.append(
        "[Planner] Plan created successfully."
    )

    return {
        "plan": plan,
        "logs": logs
    }


# ---------------------------
# Executor Node
# ---------------------------

def executor_node(state: AgentState):

    logs = state["logs"]

    logs.append(
        "[Executor] Opening browser..."
    )

    result = execute_task(
        state["task"]
    )

    logs.append(
        "[Executor] Research completed."
    )

    return {
        "execution_result": result,
        "logs": logs
    }


# ---------------------------
# Summarizer Node
# ---------------------------

def summarizer_node(state: AgentState):

    logs = state["logs"]

    logs.append(
        "[Summarizer] Summarizing content..."
    )

    summary = summarize_content(
        state["execution_result"]
    )

    logs.append(
        "[Summarizer] Summary generated."
    )

    return {
        "summary": summary,
        "logs": logs
    }


# ---------------------------
# Email Node
# ---------------------------

def email_node(state: AgentState):

    logs = state["logs"]

    if state["email_requested"]:

        logs.append(
            "[Email Agent] Sending email..."
        )

        email_summary(
            state["recipient"],
            state["summary"]
        )

        logs.append(
            "[Email Agent] Email sent successfully."
        )

    else:

        logs.append(
            "[Email Agent] No email requested."
        )

    return {
        "logs": logs
    }


# ---------------------------
# Calendar Node
# ---------------------------

def calendar_node(state: AgentState):

    logs = state["logs"]

    if state["calendar_requested"]:

        logs.append(
            "[Calendar Agent] Extracting meeting details..."
        )

        details = extract_calendar_details(
            state["task"]
        )

        print("Calendar Details:")
        print(details)

        if details:

            try:

                # Validate fields
                title = details.get("title")
                date = details.get("date")
                time = details.get("time")

                if not title or not date or not time:

                    logs.append(
                        "[Calendar Agent] Missing required fields."
                    )

                    return {
                        "logs": logs
                    }

                # Safe duration parsing
                try:

                    duration = int(
                        details.get(
                            "duration_hours",
                            1
                        )
                    )

                except:

                    duration = 1

                # Prevent invalid durations
                if duration <= 0:

                    duration = 1

                # Safe datetime creation
                start = datetime.fromisoformat(
                    f"{date}T{time}:00"
                )

                end = start + timedelta(
                    hours=duration
                )

                print("Start Time:", start)
                print("End Time:", end)
                print("Duration:", duration)

                # Final safety check
                if end <= start:

                    logs.append(
                        "[Calendar Agent] Invalid time range."
                    )

                    return {
                        "logs": logs
                    }

                # Create Google Calendar event
                create_calendar_event(
                    title,
                    start,
                    end
                )

                logs.append(
                    "[Calendar Agent] Meeting scheduled successfully."
                )

            except Exception as e:

                logs.append(
                    f"[Calendar Agent] Failed: {str(e)}"
                )

        else:

            logs.append(
                "[Calendar Agent] Could not extract meeting details."
            )

    else:

        logs.append(
            "[Calendar Agent] No calendar action requested."
        )

    return {
        "logs": logs
    }


# ---------------------------
# Build Graph
# ---------------------------

graph = StateGraph(AgentState)

# Nodes
graph.add_node(
    "planner",
    planner_node
)

graph.add_node(
    "executor",
    executor_node
)

graph.add_node(
    "summarizer",
    summarizer_node
)

graph.add_node(
    "email",
    email_node
)

graph.add_node(
    "calendar",
    calendar_node
)

# Entry point
graph.set_entry_point("planner")

# Workflow edges
graph.add_edge(
    "planner",
    "executor"
)

graph.add_edge(
    "executor",
    "summarizer"
)

graph.add_edge(
    "summarizer",
    "email"
)

graph.add_edge(
    "email",
    "calendar"
)

graph.add_edge(
    "calendar",
    END
)

# Compile workflow
workflow = graph.compile()