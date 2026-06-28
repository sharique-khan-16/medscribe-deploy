"""SQLite database management layer."""

import os
import sqlite3
from typing import Dict, Any, List
from src.extractor import ExtractionResult

DB_PATH = os.path.join("data", "medscribe.db")


def get_connection():
    """Return a SQLite connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the SQLite database tables if they do not exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with get_connection() as conn:
        # 1. Patients Table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                age INTEGER,
                gender TEXT
            );
        """)

        # 2. Records Table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('prescription', 'lab_report')),
                date TEXT,
                doctor_name TEXT,
                facility TEXT,
                diagnosis TEXT,
                extraction_confidence TEXT NOT NULL CHECK(extraction_confidence IN ('high', 'medium', 'low')),
                FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
            );
        """)

        # 3. Medications Table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                dosage TEXT NOT NULL,
                frequency TEXT NOT NULL,
                duration TEXT,
                FOREIGN KEY (record_id) REFERENCES records (id) ON DELETE CASCADE
            );
        """)

        # 4. Lab Results Table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lab_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                test_name TEXT NOT NULL,
                value TEXT NOT NULL,
                unit TEXT,
                reference_range TEXT,
                flag TEXT CHECK(flag IN ('normal', 'high', 'low') OR flag IS NULL),
                FOREIGN KEY (record_id) REFERENCES records (id) ON DELETE CASCADE
            );
        """)
        conn.commit()


def save_extraction(result: ExtractionResult) -> int:
    """Save an ExtractionResult into the database, split across tables.

    Returns:
        The ID of the newly inserted record.
    """
    init_db()  # Ensure database and tables exist

    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Insert or update patient
        cursor.execute(
            """
            INSERT INTO patients (name, age, gender)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                age = COALESCE(excluded.age, patients.age),
                gender = COALESCE(excluded.gender, patients.gender)
            RETURNING id;
            """,
            (result.patient.name, result.patient.age, result.patient.gender),
        )
        patient_row = cursor.fetchone()
        if patient_row:
            patient_id = patient_row["id"]
        else:
            # Fallback if RETURNING clause is not supported on old sqlite versions
            cursor.execute(
                "SELECT id FROM patients WHERE name = ?;", (result.patient.name,)
            )
            patient_id = cursor.fetchone()["id"]

        # 2. Insert record
        cursor.execute(
            """
            INSERT INTO records (patient_id, type, date, doctor_name, facility, diagnosis, extraction_confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (
                patient_id,
                result.record.type,
                result.record.date,
                result.record.doctor_name,
                result.record.facility,
                result.diagnosis,
                result.extraction_confidence,
            ),
        )
        record_id = cursor.lastrowid

        # 3. Insert medications
        for med in result.medications:
            cursor.execute(
                """
                INSERT INTO medications (record_id, name, dosage, frequency, duration)
                VALUES (?, ?, ?, ?, ?);
                """,
                (record_id, med.name, med.dosage, med.frequency, med.duration),
            )

        # 4. Insert lab results
        for lab in result.lab_results:
            cursor.execute(
                """
                INSERT INTO lab_results (record_id, test_name, value, unit, reference_range, flag)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    record_id,
                    lab.test_name,
                    lab.value,
                    lab.unit,
                    lab.reference_range,
                    lab.flag,
                ),
            )

        conn.commit()
        return record_id


def get_all_records() -> list[dict[str, Any]]:
    """Query and return all medical records reconstructed with patient and relation data."""
    init_db()
    records_list = []

    with get_connection() as conn:
        cursor = conn.cursor()
        # Query main record and patient info
        cursor.execute("""
            SELECT r.id as record_id, r.type, r.date, r.doctor_name, r.facility, r.diagnosis, r.extraction_confidence,
                   p.name as patient_name, p.age as patient_age, p.gender as patient_gender
            FROM records r
            JOIN patients p ON r.patient_id = p.id
            ORDER BY r.id DESC;
            """)
        rows = cursor.fetchall()

        for row in rows:
            record_id = row["record_id"]

            # Fetch medications for this record
            cursor.execute(
                "SELECT name, dosage, frequency, duration FROM medications WHERE record_id = ?;",
                (record_id,),
            )
            medications = [dict(m) for m in cursor.fetchall()]

            # Fetch lab results for this record
            cursor.execute(
                "SELECT test_name, value, unit, reference_range, flag FROM lab_results WHERE record_id = ?;",
                (record_id,),
            )
            lab_results = [dict(lab_row) for lab_row in cursor.fetchall()]

            records_list.append(
                {
                    "id": record_id,
                    "patient": {
                        "name": row["patient_name"],
                        "age": row["patient_age"],
                        "gender": row["patient_gender"],
                    },
                    "record": {
                        "type": row["type"],
                        "date": row["date"],
                        "doctor_name": row["doctor_name"],
                        "facility": row["facility"],
                    },
                    "diagnosis": row["diagnosis"],
                    "medications": medications,
                    "lab_results": lab_results,
                    "extraction_confidence": row["extraction_confidence"],
                }
            )

    return records_list
