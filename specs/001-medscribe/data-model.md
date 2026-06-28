# Data Model Specification: MedScribe Output Schema

This document defines the structured JSON data schema that the local SLM must return and that the local SQLite database must store.

---

## 📋 Schema Definition (JSON)

```json
{
  "patient": {
    "name": "string",
    "age": "number | null",
    "gender": "string | null"
  },
  "record": {
    "type": "prescription | lab_report",
    "date": "string (ISO 8601) | null",
    "doctor_name": "string | null",
    "facility": "string | null"
  },
  "medications": [
    {
      "name": "string",
      "dosage": "string",
      "frequency": "string",
      "duration": "string | null"
    }
  ],
  "diagnosis": "string | null",
  "lab_results": [
    {
      "test_name": "string",
      "value": "string",
      "unit": "string | null",
      "reference_range": "string | null",
      "flag": "normal | high | low | null"
    }
  ],
  "extraction_confidence": "high | medium | low"
}
```

---

## 🔍 Schema Details

### 1. `patient` (Object)
*   `name` (string, required): Full name of the patient.
*   `age` (integer or null, required): Age of the patient. Set to `null` if not detected.
*   `gender` (string or null, required): Gender of the patient (e.g. "Male", "Female", "Other"). Set to `null` if not detected.

### 2. `record` (Object)
*   `type` (string, required): Must be either `"prescription"` or `"lab_report"`.
*   `date` (string or null, required): The date the document was generated, represented as an ISO 8601 datetime string. Set to `null` if not found.
*   `doctor_name` (string or null, required): Name of the doctor who issued the prescription or ordered the lab test. Set to `null` if not found.
*   `facility` (string or null, required): Name of the clinic, hospital, or diagnostic center. Set to `null` if not found.

### 3. `medications` (Array of Objects)
*   `name` (string, required): Name of the drug/medication.
*   `dosage` (string, required): Dosage instructions (e.g. "500mg", "1 tablet").
*   `frequency` (string, required): Frequency of administration (e.g. "twice daily", "once every 8 hours").
*   `duration` (string or null, required): Duration of treatment (e.g. "7 days", "1 month"). Set to `null` if not specified.

### 4. `diagnosis` (String or Null)
*   `diagnosis` (string or null, required): Primary diagnosis or reason for prescription/lab test. Set to `null` if not found.

### 5. `lab_results` (Array of Objects)
*   `test_name` (string, required): Name of the laboratory test (e.g. "Hemoglobin", "WBC").
*   `value` (string, required): Numeric or qualitative value of the test result.
*   `unit` (string or null, required): Unit of measurement (e.g. "g/dL", "million/uL"). Set to `null` if not specified.
*   `reference_range` (string or null, required): Reference range indicating normal values (e.g. "12.0 - 16.0"). Set to `null` if not specified.
*   `flag` (string or null, required): Assessment flag. Must be either `"normal"`, `"high"`, `"low"`, or `null`.

### 6. `extraction_confidence` (String)
*   `extraction_confidence` (string, required): Assessment of extraction quality. Must be either `"high"`, `"medium"`, or `"low"`.
