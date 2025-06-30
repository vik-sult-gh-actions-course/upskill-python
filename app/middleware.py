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
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def log_requests(request: Request, call_next):
    start_time = datetime.now()

    method = request.method
    path = request.url.path
    query_params = dict(request.query_params)
    client_host = request.client.host if request.client else "unknown"

    logger.info(
        f"Incoming request - Method: {method}, Path: {path}, "
        f"Query: {query_params}, Client: {client_host}"
    )

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Request error: {str(e)}")
        raise

    process_time = (datetime.now() - start_time).total_seconds() * 1000
    logger.info(
        f"Request completed - Method: {method}, Path: {path}, "
        f"Status: {response.status_code}, Duration: {process_time:.2f}ms"
    )

    return response