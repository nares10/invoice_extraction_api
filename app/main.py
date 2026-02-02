from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader

from app.extractor import extract_invoice_data
from app.schema import InvoiceResponse, NonInvoiceResponse , DocumentResponse
from app.validators import validate_pdf
import pickle

app = FastAPI(
    title="Invoice Extraction API",
    description="Extract structured data from invoice PDFs",
    version="1.0"
)

with open("model/doc_classifier_v1.pkl", "rb") as f:
    doc_classifier = pickle.load(f)

def extract_text_from_pdf(file: UploadFile) -> str:
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

@app.post("/analyze", response_model=DocumentResponse)
async def analyze_invoice(file: UploadFile = File(...)):
    validate_pdf(file)

    text = extract_text_from_pdf(file)
    doc_type = doc_classifier.predict([text])[0]
    print(doc_classifier.predict([text]))

    if doc_type != "invoice":
        return NonInvoiceResponse(
            document_type="non-invoice",
            #confidence=confidence
        )

    
    extracted_data = extract_invoice_data(text)
    
    return InvoiceResponse(
        document_type="invoice",
        **extracted_data
    )