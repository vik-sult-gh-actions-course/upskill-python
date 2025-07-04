"""
Main Application Module

This module initializes the FastAPI application, configures custom middleware,
defines health check endpoint, and includes application routers.

The application uses FastAPI as the web framework and extends functionality through
custom middleware for request logging and response timing. The primary API routes
are organized in separate modules and are included here.

Key components:
- FastAPI instance `app` with metadata and middleware setup.
- Middleware: Adds process time header and logs incoming requests.
- Health check endpoint: Provides a simple endpoint to verify service availability.
- Routers: API routes defined in modular files (e.g., task router).
"""

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from .middleware import add_process_time_header, log_requests
from .routers import task

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)


@app.get("/healthy")
def health_check():
    """
    Health check endpoint.

    Returns:
        dict: A simple status message indicating the service is healthy.
    """
    return {"status": "Healthy"}


app.include_router(task.router)
