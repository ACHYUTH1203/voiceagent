import os
import random
from datetime import datetime, timedelta

from faker import Faker
from dotenv import load_dotenv

from sqlalchemy import create_engine, text

# ==========================================
# CONFIG
# ==========================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")

# Added use_insertmanyvalues=True to speed up bulk inserts
engine = create_engine(
    DATABASE_URL, 
    use_insertmanyvalues=True
)

fake = Faker()

NUM_RECORDS = 100
START_DATE = datetime.now() - timedelta(days=30)

# ==========================================
# DATA RULES
# ==========================================

INTENTS = [
    "product_information",
    "pricing_query",
    "integration_query",
    "schedule_demo",
    "support_request",
    "lead_qualification"
]

OUTCOMES = [
    "qualified_lead",
    "unqualified_lead",
    "follow_up_required",
    "support_resolved",
    "human_handoff"
]

SENTIMENTS = [
    "positive",
    "neutral",
    "negative"
]

INDUSTRIES = [
    "Real Estate",
    "Healthcare",
    "E-commerce",
    "SaaS",
    "Financial Services"
]

CRMS = [
    "Salesforce",
    "Zoho",
    "HubSpot",
    "Freshworks",
    "None"
]

PAIN_POINTS = [
    "Too many missed calls",
    "Manual follow-ups taking too long",
    "High support costs",
    "No CRM integration"
]

# ==========================================
# TABLE CREATION
# ==========================================

def create_table_if_not_exists():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS call_analytics (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

            session_id UUID NOT NULL,
            started_at TIMESTAMPTZ NOT NULL,

            duration_seconds INTEGER,
            total_turns INTEGER,

            final_intent VARCHAR(255),
            intent_confidence NUMERIC(5,2),

            sentiment VARCHAR(50),
            call_outcome VARCHAR(100),

            lead_industry VARCHAR(255),
            lead_crm VARCHAR(255),

            lead_call_volume INTEGER,
            lead_score INTEGER,

            lead_pain_points TEXT,

            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
        """))

# ==========================================
# GENERATE DATA
# ==========================================

def generate_records():
    records = []

    for _ in range(NUM_RECORDS):

        days_offset = random.randint(0, 30)

        hour = random.choices(
            population=list(range(24)),
            weights=[
                1,1,1,1,1,1,
                3,10,15,15,15,15,
                15,15,15,10,8,5,
                3,2,1,1,1,1
            ],
            k=1
        )[0]

        started_at = START_DATE + timedelta(
            days=days_offset,
            hours=hour,
            minutes=random.randint(0, 59)
        )

        outcome = random.choices(
            OUTCOMES,
            weights=[30, 20, 15, 25, 10]
        )[0]

        if outcome == "qualified_lead":
            duration = random.randint(180, 600)
            turns = random.randint(10, 25)
            sentiment = random.choices(
                SENTIMENTS,
                weights=[70, 25, 5]
            )[0]
            lead_score = random.randint(60, 100)
            crm = random.choices(
                CRMS,
                weights=[40, 20, 30, 10, 0]
            )[0]

        else:
            duration = random.randint(30, 180)
            turns = random.randint(2, 8)
            sentiment = random.choices(
                SENTIMENTS,
                weights=[10, 60, 30]
            )[0]
            lead_score = random.randint(0, 40)
            crm = random.choice(CRMS)

        records.append({
            "session_id": str(fake.uuid4()),
            "started_at": started_at,
            "duration_seconds": duration,
            "total_turns": turns,
            "final_intent": random.choice(INTENTS),
            "intent_confidence": round(
                random.uniform(0.75, 0.99),
                2
            ),
            "sentiment": sentiment,
            "call_outcome": outcome,
            "lead_industry": random.choice(INDUSTRIES),
            "lead_crm": crm,
            "lead_call_volume": random.randint(100, 10000),
            "lead_score": lead_score,
            "lead_pain_points": random.choice(PAIN_POINTS),
        })

    return records

# ==========================================
# INSERT INTO POSTGRES
# ==========================================

INSERT_QUERY = text("""
INSERT INTO call_analytics (
    session_id,
    started_at,
    duration_seconds,
    total_turns,
    final_intent,
    intent_confidence,
    sentiment,
    call_outcome,
    lead_industry,
    lead_crm,
    lead_call_volume,
    lead_score,
    lead_pain_points
)
VALUES (
    :session_id,
    :started_at,
    :duration_seconds,
    :total_turns,
    :final_intent,
    :intent_confidence,
    :sentiment,
    :call_outcome,
    :lead_industry,
    :lead_crm,
    :lead_call_volume,
    :lead_score,
    :lead_pain_points
)
""")

def upload_data(records):
    with engine.begin() as conn:
        conn.execute(INSERT_QUERY, records)

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    
    print("Setting up database schema...")
    create_table_if_not_exists()

    print(f"Generating {NUM_RECORDS} records...")
    records = generate_records()

    print("Uploading to PostgreSQL...")
    upload_data(records)

    print("✅ Successfully created schema and inserted records!")