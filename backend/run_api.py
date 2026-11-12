import uvicorn
from dotenv import load_dotenv
import os
load_dotenv()

def get_api_host():
    return os.getenv("API_HOST", "localhost")

def get_api_port():
    port = os.getenv("API_PORT", "8000")
    return int(port)

def get_api_reload():
    return os.getenv("API_RELOAD", "false").lower() == "true"

def run_api():
    uvicorn.run("api:app", host = get_api_host(), port = get_api_port(), reload = get_api_reload())

if __name__ == "__main__":
    run_api()