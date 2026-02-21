import sys
import subprocess
import time
import requests
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
load_dotenv()

BACKEND_URL = "http://127.0.0.1:8000/docs"

def wait_for_backend(timeout=30):
    logger.info("Waiting for backend to be ready...")
    start = time.time()

    while time.time() - start < timeout:
        try:
            r = requests.get(BACKEND_URL)
            if r.status_code == 200:
                logger.info("Backend is ready")
                return
        except Exception:
            pass
        time.sleep(1)

    raise RuntimeError("Backend did not start in time")

def run_backend():
    logger.info("Starting backend service...")
    subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            "app.backend.api:app",
            "--host", "127.0.0.1",
            "--port", "8000",
        ]
    )

def run_frontend():
    logger.info("Starting frontend service...")
    subprocess.Popen(
        [
            sys.executable, "-m", "streamlit",
            "run", "app/frontend/ui.py",
        ]
    )

if __name__ == "__main__":
    try:
        run_backend()
        wait_for_backend()
        run_frontend()
    except Exception as e:
        logger.error("Application startup failed")
        raise CustomException("Failed to start application", e)


    
