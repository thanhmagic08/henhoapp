from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "users_data.json")

def load_users_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/group_messages")
def get_group_messages():
    data = load_users_data()
    return {"group_messages": data.get("group_messages", [])}


def run_api(host: str = "0.0.0.0", port: int = 8502):
    uvicorn.run(app, host=host, port=port, log_level="info")


def start_api_in_thread(host: str = "0.0.0.0", port: int = 8502):
    t = threading.Thread(target=run_api, args=(host, port), daemon=True)
    t.start()
    return t
