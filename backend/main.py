from fastapi import FastAPI
from pydantic import BaseModel

from workflows.graph import workflow

app = FastAPI()


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
        "summary": ""
    })

    return result