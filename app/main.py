from fastapi import FastAPI
from app.routers import endpoints, steps, tests
from app.tasks import run_test_task
from celery.result import AsyncResult
from app.celery_app import celery_app

app = FastAPI()

app.include_router(endpoints.router, prefix="/api", tags=["endpoints"])
app.include_router(steps.router, prefix="/api", tags=["steps"])
app.include_router(tests.router, prefix="/api", tags=["tests"])

@app.post("/run_test/{test_id}")
def run_test_endpoint(test_id: int):
    result = run_test_task.delay(test_id)
    return {"task_id": result.id}

@app.get("/task_status/{task_id}")
def task_status_endpoint(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "status": result.status, "result": str(result.result)}
