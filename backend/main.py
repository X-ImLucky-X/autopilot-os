from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from workflows.graph import workflow
from agents.router_agent import classify_task


app = FastAPI()


# ---------------------------
# CORS
# ---------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------
# Request Model
# ---------------------------

class TaskRequest(BaseModel):

    task: str


# ---------------------------
# Health Route
# ---------------------------

@app.get("/")
def home():

    return {
        "message": "PilotOS Backend Running"
    }


# ---------------------------
# Main Task Route
# ---------------------------

@app.post("/task")
def run_task(request: TaskRequest):

    # ---------------------------
    # AI Router Decision
    # ---------------------------

    tool_decision = classify_task(
        request.task
    )

    print("Tool Decision:")
    print(tool_decision)

    # ---------------------------
    # Extract Tool Decisions
    # ---------------------------

    email_requested = tool_decision.get(
        "email",
        False
    )

    recipient = tool_decision.get(
        "recipient",
        ""
    )

    calendar_requested = tool_decision.get(
        "calendar",
        False
    )

    # ---------------------------
    # Run Workflow
    # ---------------------------

    result = workflow.invoke({

        # User Task
        "task": request.task,

        # Tool Decisions
        "tool_decision": str(tool_decision),

        # Email
        "email_requested": email_requested,
        "recipient": recipient,

        # Calendar
        "calendar_requested": calendar_requested,
        "calendar_details": {},

        # Workflow Outputs
        "plan": "",
        "execution_result": "",
        "summary": "",

        # Logs
        "logs": []
    })

    return result