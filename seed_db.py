# data/seed_db.py
import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME", "clinicalops")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

print(f"🗄️  Connected to MongoDB: {DB_NAME}")

# 1. Seed Patients
patients = [
    {
        "patient_id": "PAT-001",
        "birth_date": "1988-04-12",
        "gender": "female",
        "conditions": ["C50.911", "E11.9"],
        "medications": ["Metformin 500mg BID", "Tamoxifen 20mg Daily"],
        "labs": {"HbA1c": 6.8, "Creatinine": 0.9, "ECOG": 1},
        "summary": "37yo female with HR+ breast cancer, well-controlled T2DM, ECOG 1"
    },
    {
        "patient_id": "PAT-002",
        "birth_date": "1965-11-03",
        "gender": "male",
        "conditions": ["C34.1", "I10"],
        "medications": ["Lisinopril 10mg", "Omeprazole 20mg"],
        "labs": {"HbA1c": 5.4, "Creatinine": 1.1, "ECOG": 0},
        "summary": "59yo male with NSCLC stage III, hypertension, ECOG 0"
    }
]
db.patients.insert_many(patients)
print(f"✅ Inserted {len(patients)} patients")

# 2. Seed Trial Protocols
trials = [
    {
        "trial_id": "ONCO-BR-01",
        "name": "Phase II Targeted Therapy for HR+ Breast Cancer",
        "criteria": [
            {"type": "inclusion", "text": "Age 18-75 years"},
            {"type": "inclusion", "text": "HR+ breast cancer confirmed"},
            {"type": "inclusion", "text": "ECOG 0-1"},
            {"type": "exclusion", "text": "HbA1c > 7.5%"},
            {"type": "exclusion", "text": "Creatinine > 1.5 mg/dL"}
        ],
        "status": "active"
    },
    {
        "trial_id": "IMMUNE-LU-07",
        "name": "Checkpoint Inhibitor Combo for NSCLC",
        "criteria": [
            {"type": "inclusion", "text": "Stage III/IV NSCLC"},
            {"type": "inclusion", "text": "ECOG 0-1"},
            {"type": "exclusion", "text": "Active autoimmune disease"},
            {"type": "exclusion", "text": "HbA1c > 8.0%"}
        ],
        "status": "active"
    }
]
db.trials.insert_many(trials)
print(f"✅ Inserted {len(trials)} trials")

# 3. Seed Adverse Events (Mock)
aes = [
    {
        "ae_id": "AE-001",
        "patient_id": "PAT-001",
        "trial_id": "ONCO-BR-01",
        "description": "Mild fatigue, day 4 post-dose. CTCAE Grade 1.",
        "severity": "mild",
        "is_sae": False,
        "reported_date": datetime.utcnow().isoformat()
    },
    {
        "ae_id": "AE-002",
        "patient_id": "PAT-002",
        "trial_id": "IMMUNE-LU-07",
        "description": "Severe rash requiring ER visit, unable to tolerate oral meds. CTCAE Grade 3.",
        "severity": "severe",
        "is_sae": True,
        "reported_date": datetime.utcnow().isoformat()
    }
]
db.adverse_events.insert_many(aes)
print(f"✅ Inserted {len(aes)} adverse events")

print("\n🎉 Database seeded successfully! Ready for agent testing.")
client.close()