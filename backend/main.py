from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from workflows.graph import workflow

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class TaskRequest(BaseModel):
    task: str


@app.get("/")
def home():

    return {
        "message": "AutoPilot OS Backend Running"
    }


@app.post("/task")
def run_task(request: TaskRequest):

    result = workflow.invoke({

        "task": request.task,
        "plan": "",
        "execution_result": "",
        "summary": "",
        "logs": []
    })

    return result