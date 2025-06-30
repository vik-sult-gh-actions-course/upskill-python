from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from .middleware import add_process_time_header, log_requests
from .routers import task

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(task.router)
