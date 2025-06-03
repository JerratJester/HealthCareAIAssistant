"""
Mock FHIR handlers + in-memory data store
"""

from typing import List, Dict
import uuid

# ──────────────────── Sample data ───────────────────────────
_PATIENTS: List[Dict] = [
    {"id": "p123", "name": "Alice Smith",  "dob": "1985-02-10", "allergies": ["penicillin"]},
    {"id": "p456", "name": "Bob Jones",    "dob": "1972-11-05", "allergies": []},
    {"id": "p789", "name": "Carol Lee",    "dob": "1990-07-22", "allergies": ["latex", "nuts"]},
    {"id": "p101", "name": "David Kim",    "dob": "1965-12-15", "allergies": ["aspirin"]},
    {"id": "p202", "name": "Eva Martinez", "dob": "1978-03-30", "allergies": ["shellfish"]},
    {"id": "p303", "name": "Frank Zhao",   "dob": "1982-09-12", "allergies": ["gluten", "pollen"]},
]

_APPOINTMENTS: List[Dict] = [
    {"id": "a1", "patientId": "p123", "surgeon": "Dr. Taylor",    "datetime": "2025-06-01T08:00:00", "procedure": "Appendectomy"},
    {"id": "a2", "patientId": "p456", "surgeon": "Dr. Lee",       "datetime": "2025-06-01T10:30:00", "procedure": "Gallbladder Removal"},
    {"id": "a3", "patientId": "p789", "surgeon": "Dr. Patel",     "datetime": "2025-06-02T09:00:00", "procedure": "Hip Replacement"},
    {"id": "a4", "patientId": "p101", "surgeon": "Dr. Wong",      "datetime": "2025-06-02T13:00:00", "procedure": "Knee Arthroscopy"},
    {"id": "a5", "patientId": "p202", "surgeon": "Dr. Hernandez", "datetime": "2025-06-03T11:00:00", "procedure": "Cataract Surgery"},
    {"id": "a6", "patientId": "p303", "surgeon": "Dr. Robinson",  "datetime": "2025-06-03T15:30:00", "procedure": "Tonsillectomy"},
]

# ──────────────────── Patient helpers ───────────────────────
def list_patients() -> List[Dict]:
    return [{"resourceType": "Patient", **p} for p in _PATIENTS]

def get_patient(patient_id: str) -> Dict:
    for p in _PATIENTS:
        if p["id"] == patient_id:
            return {"resourceType": "Patient", **p}
    return {}

def add_patient(patient_data: Dict) -> Dict:
    new_id = f"p{uuid.uuid4().hex[:6]}"
    record = {"id": new_id, **patient_data}
    _PATIENTS.append(record)
    return {"resourceType": "Patient", **record}

# ──────────────────── Appointment helpers ───────────────────
def get_appointments(date: str) -> List[Dict]:
    return [
        {"resourceType": "Appointment", **a}
        for a in _APPOINTMENTS
        if a["datetime"].startswith(date)
    ]

def add_appointment(appt_data: Dict) -> Dict:
    new_id = f"a{uuid.uuid4().hex[:6]}"
    record = {"id": new_id, **appt_data}
    _APPOINTMENTS.append(record)
    return {"resourceType": "Appointment", **record}

def update_appointment(appointment_id: str, updates: Dict) -> Dict:
    for i, a in enumerate(_APPOINTMENTS):
        if a["id"] == appointment_id:
            _APPOINTMENTS[i] = {**a, **updates}
            return {"resourceType": "Appointment", **_APPOINTMENTS[i]}
    return {}

def delete_appointment(appointment_id: str) -> bool:
    for a in list(_APPOINTMENTS):
        if a["id"] == appointment_id:
            _APPOINTMENTS.remove(a)
            return True
    return False
