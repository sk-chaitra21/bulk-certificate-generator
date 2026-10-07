# Bulk Certificate Generator API

A backend API that accepts bulk certificate generation requests, validates recipient data, generates certificates using a predefined template, tracks individual certificate status, and allows generated certificates to be retrieved.

## Features

- Bulk certificate generation
- Recipient data validation
- PostgreSQL database
- FastAPI REST APIs
- SQLAlchemy ORM
- PDF certificate generation using ReportLab
- Individual certificate status tracking
- Job-level success/failure tracking
- Failure isolation between recipients
- Certificate download API
- Automated API tests using Pytest
- Interactive Swagger API documentation

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- ReportLab
- Pytest
- Uvicorn

## Project Structure

```text
bulk-certificate-generator/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── generation.py
│   │       └── certificates.py
│   │
│   ├── core/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── generation_job.py
│   │   └── certificate.py
│   │
│   ├── schemas/
│   │   └── generation.py
│   │
│   ├── services/
│   │   └── certificate_service.py
│   │
│   └── main.py
│
├── generated_certificates/
├── templates/
├── tests/
│   └── test_api.py
│
├── .env
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md