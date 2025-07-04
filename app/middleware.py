"""
Middleware utilities for FastAPI application.

This module provides middleware functions for:
    - Adding the X-Process-Time header to responses, indicating request processing time.
    - Logging incoming HTTP requests and their completion status.

Requires:
    - FastAPI
    - Python logging
"""
import logging
import time
from datetime import datetime

from fastapi import Request

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def add_process_time_header(request: Request, call_next):
    """
    Middleware to add the X-Process-Time header to the response.

    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable): The next middleware or route handler.

    Returns:
        Response: The HTTP response with the X-Process-Time header.
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def log_requests(request: Request, call_next):
    """
    Middleware to log details about each HTTP request and its response.

    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable): The next middleware or route handler.

    Returns:
        Response: The HTTP response after logging request and response details.
    """
    start_time = datetime.now()

    method = request.method
    path = request.url.path
    query_params = dict(request.query_params)
    client_host = request.client.host if request.client else "unknown"

    logger.info(
        "Incoming request - Method: %s, Path: %s, Query: %s, Client: %s",
        method, path, query_params, client_host
    )

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error("Request error: %s", str(e))
        raise

    process_time = (datetime.now() - start_time).total_seconds() * 1000
    logger.info(
        "Request completed - Method: %s, Path: %s, Status: %s, Duration: %.2fms",
        method, path, response.status_code, process_time
    )

    return response
