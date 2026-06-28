"""Ollama Extraction and Validation Module."""

import json
import logging
from typing import Literal
from pydantic import BaseModel, Field, ValidationError
import ollama

# Configure logger
logger = logging.getLogger("medscribe.extractor")


class PatientModel(BaseModel):
    name: str
    age: int | None = None
    gender: str | None = None


class RecordModel(BaseModel):
    type: Literal["prescription", "lab_report"]
    date: str | None = None
    doctor_name: str | None = None
    facility: str | None = None


class MedicationModel(BaseModel):
    name: str
    dosage: str
    frequency: str
    duration: str | None = None


class LabResultModel(BaseModel):
    test_name: str
    value: str
    unit: str | None = None
    reference_range: str | None = None
    flag: Literal["normal", "high", "low"] | None = None


class ExtractionResult(BaseModel):
    patient: PatientModel
    record: RecordModel
    medications: list[MedicationModel] = Field(default_factory=list)
    diagnosis: str | None = None
    lab_results: list[LabResultModel] = Field(default_factory=list)
    extraction_confidence: Literal["high", "medium", "low"]


# Base prompt template
PROMPT_TEMPLATE = """You are a medical data extraction system. You are given raw OCR text from a medical document.
Your task is to extract patient information, record type, medications, diagnoses, and lab results into a JSON object matching this schema exactly:

{schema}

Strict constraints:
- Return ONLY valid JSON matching the schema.
- Do NOT wrap your response in markdown code blocks like ```json ... ```. Return raw JSON string.
- If record type cannot be determined, default to "prescription".
- If a value is missing, use null (or an empty list for arrays).
- extraction_confidence must be "high", "medium", or "low".

Guidelines for extraction:
- patient.name: Extract the patient's name (often prefixed by 'Name:', e.g., 'Maria Sharapova'). Do NOT use the doctor's name here.
- record.doctor_name: Extract the doctor's name (often prefixed by 'Dr', e.g., 'Dr John Smith').
- record.facility: Extract the hospital, clinic, or city location.
- medications: Search the OCR text for drug names (e.g., 'Prednisone', 'Liatda'). For each medication, extract:
  * name: the drug name.
  * dosage: the strength or amount (e.g., '20 mg', '2.4 gram'). If not found, default to "not specified".
  * frequency: frequency instruction. If not found, default to "not specified" or "as directed".
  * duration: duration of treatment (e.g., '3 days', '1 month'). If not found, use null.

Here is an example:

Example Input Raw OCR Text:
Name: John Doe
Date: 12/12/2023
Doctor: Dr. Jane Doe
Facility: Grace Clinic
Diagnosis: Hypertension
Medications:
Amlodipine 5mg once daily
Metoprolol 50mg

Example Output JSON:
{{
  "patient": {{
    "name": "John Doe",
    "age": null,
    "gender": null
  }},
  "record": {{
    "type": "prescription",
    "date": "2023-12-12T00:00:00Z",
    "doctor_name": "Dr. Jane Doe",
    "facility": "Grace Clinic"
  }},
  "medications": [
    {{
      "name": "Amlodipine",
      "dosage": "5mg",
      "frequency": "once daily",
      "duration": null
    }},
    {{
      "name": "Metoprolol",
      "dosage": "50mg",
      "frequency": "not specified",
      "duration": null
    }}
  ],
  "diagnosis": "Hypertension",
  "lab_results": [],
  "extraction_confidence": "high"
}}

Raw OCR Text to process:
{text}
"""


def extract_data(ocr_text: str) -> ExtractionResult:
    """Send OCR text to Ollama, parse and validate the output against the Pydantic schema.

    Retries once with error details if parsing or validation fails. Returns a fallback
    object with confidence "low" if it fails twice.
    """
    model_name = "qwen2.5:1.5b"
    schema_str = json.dumps(ExtractionResult.model_json_schema(), indent=2)
    prompt = PROMPT_TEMPLATE.format(schema=schema_str, text=ocr_text)

    try:
        # First attempt
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.0},
        )
        content = response["message"]["content"].strip()
        return parse_and_validate(content)

    except (json.JSONDecodeError, ValidationError, Exception) as first_err:
        logger.warning(
            f"First extraction attempt failed: {first_err}. Retrying once..."
        )

        # Construct retry prompt with error feedback
        retry_prompt = (
            prompt
            + f"\n\nYour previous response failed validation with the following error:\n{str(first_err)}\n"
            + "Please correct the output and return ONLY the valid JSON object."
        )

        try:
            # Second attempt
            response = ollama.chat(
                model=model_name,
                messages=[{"role": "user", "content": retry_prompt}],
                options={"temperature": 0.0},
            )
            content = response["message"]["content"].strip()
            return parse_and_validate(content)

        except Exception as second_err:
            logger.error(
                f"Second extraction attempt failed: {second_err}. Returning fallback result."
            )
            # Fallback graceful error object
            return ExtractionResult(
                patient=PatientModel(name="Unknown"),
                record=RecordModel(type="prescription"),
                extraction_confidence="low",
                diagnosis=f"Extraction failed: {second_err}",
            )


def parse_and_validate(content: str) -> ExtractionResult:
    """Helper to parse a JSON string and validate it against the Pydantic model."""
    # Strip markdown block formatting if the model ignored instructions
    if content.startswith("```"):
        # Remove starting ```json or ```
        content = content.split("\n", 1)[-1]
        # Remove ending ```
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

    data = json.loads(content)
    return ExtractionResult(**data)
