from fastapi import FastAPI
import os
import uvicorn
import logging
from prometheus_client import Counter, Gauge, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response
import psutil

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Prometheus metrics
REQUEST_COUNTER = Counter("my_endpoint_api_requests_total", "Total number of API requests to my endpoint get_info", ["endpoint"])
CPU_USAGE = Gauge("my_app_cpu_usage_percent", "CPU usage of My FastAPI application")
MEMORY_USAGE = Gauge("my_app_memory_usage_bytes", "Memory usage of My FastAPI application")

@app.get("/get_info")
async def get_info():
  """
  This endpoint returns application information.
  """
  REQUEST_COUNTER.labels(endpoint="/get_info").inc()  # Increment request counter
  logger.info('get_info endpoint is called')
  app_version = os.getenv("APP_VERSION", "default_version")  # Get from environment or default
  app_title = os.getenv("APP_TITLE", "default_title")
  return {"app_version": app_version, "app_title": app_title}

@app.get('/metrics')
def metrics():
  logger.info('Metrics endpoint was called for Main App')
  # Update CPU and memory usage metrics
  process = psutil.Process()
  CPU_USAGE.set(process.cpu_percent(interval=1))
  MEMORY_USAGE.set(process.memory_info().rss)  # Resident Set Size in bytes
  return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
  import uvicorn
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
