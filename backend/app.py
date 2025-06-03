# backend/app.py
# ──────────────────────────────────────────────────────────
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.faq import lookup as faq_lookup


# Load .env (MODEL_NAME, HF_HOME, etc.)
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=False)

# ─── Internal modules ─────────────────────────────────────
from backend.chatbot.core import (
    init_chat_pipeline,
    shutdown_pipeline,
    generate_response,
)
from backend.chatbot.fhir_integration import (
    list_patients,
    get_patient,
    add_patient,
    get_appointments,
    add_appointment,
    update_appointment,
    delete_appointment,
)
# ...



# ─── FastAPI app setup ────────────────────────────────────
app = FastAPI(title="SISBot Backend", version="0.1.0")

# Allow the React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Pydantic request models ──────────────────────────────
class ChatRequest(BaseModel):
    text: str

class PatientIn(BaseModel):
    name: str
    dob: str
    allergies: List[str] = []

class AppointmentIn(BaseModel):
    patientId: str
    surgeon: str
    datetime: str
    procedure: str

# ─── Lifecycle hooks ──────────────────────────────────────
@app.on_event("startup")
def startup_event() -> None:
    init_chat_pipeline()

@app.on_event("shutdown")
def shutdown_event() -> None:
    shutdown_pipeline()

# ─── Chat endpoint ────────────────────────────────────────
@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response(req.text)
    return {"response": reply}

# ─── Patient endpoints ───────────────────────────────────
@app.get("/patients")
def patient_list():
    return {"patients": list_patients()}

@app.get("/patient/{patient_id}")
def patient_get(patient_id: str):
    patient = get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/patient")
def patient_create(data: PatientIn):
    return add_patient(data.model_dump())

# ─── Appointment endpoints ───────────────────────────────
@app.get("/schedule")
def schedule_for_date(date: str):
    return {"appointments": get_appointments(date)}

@app.post("/schedule")
def schedule_create(data: AppointmentIn):
    return add_appointment(data.model_dump())

@app.patch("/schedule/{appointment_id}")
def schedule_update(appointment_id: str, updates: AppointmentIn):
    updated = update_appointment(appointment_id, updates.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return updated

@app.delete("/schedule/{appointment_id}")
def schedule_delete(appointment_id: str):
    if not delete_appointment(appointment_id):
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"deleted": True}

@app.post("/chat")
def chat(req: ChatRequest):
    # 1) FAQ short-circuit
    for item in _FAQ:
        if req.text.strip().lower() == item["question"].lower():
            return {"response": item["answer"], "source": "faq"}
    # 2) Otherwise hit the model
    reply = generate_response(req.text)
    return {"response": reply, "source": "llm"}
@app.post("/chat")
def chat(req: ChatRequest):
    # 1. Try FAQ
    cached = faq_lookup(req.text)
    if cached:
        return {"response": cached, "source": "faq"}

    # 2. Otherwise use LLM
    reply = generate_response(req.text)
    return {"response": reply, "source": "llm"}

@app.get("/preloaded-questions")
def list_questions():
    return {"questions": get_preloaded_questions()}