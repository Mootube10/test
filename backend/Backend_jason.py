# backend/backend_json.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
from fastapi.middleware.cors import CORSMiddleware

API_SECRET = "YOUR_SECRET_KEY"  # Replace with your secret
DATA_FILE = "shifts.json"

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"]
)

class ShiftRequest(BaseModel):
    username: str
    secret: str

def load_shifts():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_shifts(shifts):
    with open(DATA_FILE, "w") as f:
        json.dump(shifts, f, indent=2)

@app.post("/shift/start")
def start_shift(data: ShiftRequest):
    if data.secret != API_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    shifts = load_shifts()
    now = datetime.utcnow().isoformat()
    shifts.append({"username": data.username, "start_time": now, "end_time": None})
    save_shifts(shifts)
    return {"status": "success", "start_time": now}

@app.post("/shift/end")
def end_shift(data: ShiftRequest):
    if data.secret != API_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    shifts = load_shifts()
    # Find last shift without end_time
    for shift in reversed(shifts):
        if shift["username"] == data.username and shift["end_time"] is None:
            shift["end_time"] = datetime.utcnow().isoformat()
            save_shifts(shifts)
            return {"status": "success", "end_time": shift["end_time"]}
    return {"status": "error", "message": "No active shift found"}

@app.get("/shifts")
def get_shifts():
    return {"shifts": load_shifts()}
