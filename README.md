# Invoice Extraction API

Lightweight FastAPI service to extract invoice fields from documents (PDF or text). This project includes a small extractor, PDF utilities, a simple classifier training script, and an API wrapper to serve the extractor.

## Features
- Extracts invoice fields such as invoice number, vendor name, invoice date, total amount, customer name, order id, and ship mode using rule-based patterns.
- PDF utilities for text extraction and preprocessing.
- Optional classifier training utilities in `model/` for dataset preparation and model experiments.
- Dockerized for easy deployment.

## Repo layout

- `app/` – application code and API:
  - `main.py` – FastAPI application entrypoint and routes.
  - `extractor.py` – rule-based extraction logic for invoice fields.
  - `pdf_utils.py` – helpers for extracting text from PDFs and preprocessing.
  - `schema.py` – request/response schemas.
  - `validators.py` – input validation helpers.
  - `config.py` – configuration values.
  - `exceptions.py` – custom exception types.
- `data/` – sample documents and helpers to build datasets.
- `model/` – training utilities (e.g. `train_classifier.py`).
- `Dockerfile` – container image build instructions.
- `requirements.txt` – Python dependencies.

## Requirements

- Python 3.10
- pip

Recommended: create a virtual environment before installing dependencies.

## Quick setup (local)

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the API locally using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open http://localhost:8000 to see the API (inspect routes in `app/main.py`).

## Docker

Build and run the container:

```bash
docker build -t invoice-extractor .
docker run -p 8000:8000 invoice-extractor
```

The service will be available on port 8000.

## Usage

Start the server then POST documents (PDF or plain text) to the API endpoint(s). See `app/main.py` for concrete route names and payload formats. Example (replace `/extract` with the actual route if different):

```bash
curl -X POST "http://localhost:8000/extract" -F "file=@/path/to/invoice.pdf"
```

Or send raw text in the JSON body depending on the API schema.

## Development notes

- The core extraction rules live in `app/extractor.py`. They use regular expressions and simple heuristics — easy to extend for new invoice formats.
- `app/pdf_utils.py` contains PDF text extraction helpers; adjust or swap the PDF backend if needed.
- `model/train_classifier.py` is a starting point for training a classifier (if you want to distinguish invoices from non-invoices or improve routing).
