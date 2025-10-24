import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///sharkflow.db")

engine: Engine = create_engine(DATABASE_URL, future=True)

def create_tables():
    with engine.begin() as conn:
        conn.execute(text('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            external_id TEXT,
            name TEXT,
            email TEXT,
            phone TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''))
        conn.execute(text('''
        CREATE TABLE IF NOT EXISTS ai_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id INTEGER,
            sentiment TEXT,
            category TEXT,
            risk_score REAL,
            extra_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(record_id) REFERENCES records(id)
        );
        '''))

def insert_record(rec: dict) -> int:
    with engine.begin() as conn:
        res = conn.execute(text('''
            INSERT INTO records (external_id, name, email, phone, notes)
            VALUES (:external_id, :name, :email, :phone, :notes)
        '''), rec)
        return res.lastrowid

def insert_ai_result(record_id: int, ai: dict):
    with engine.begin() as conn:
        conn.execute(text('''
            INSERT INTO ai_results (record_id, sentiment, category, risk_score, extra_json)
            VALUES (:record_id, :sentiment, :category, :risk_score, :extra_json)
        '''), {
            "record_id": record_id,
            "sentiment": ai.get("sentiment"),
            "category": ai.get("category"),
            "risk_score": ai.get("risk_score"),
            "extra_json": ai.get("extra_json")
        })
