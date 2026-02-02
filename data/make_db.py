import os
import csv
from pathlib import Path
from PyPDF2 import PdfReader


INVOICE_DIR = "data/invoices"
NON_INVOICE_DIR = "data/non-invoices"
OUTPUT_CSV = "data/documents.csv"

MAX_INVOICES = 25
MAX_NON_INVOICES = 20


def extract_text_from_pdf(pdf_path: Path) -> str:
    try:
        reader = PdfReader(str(pdf_path))
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return "\n".join(text)
    except Exception as e:
        print(f"[ERROR] {pdf_path.name}: {e}")
        return ""


def collect_files(directory: str, limit: int):
    pdfs = sorted(Path(directory).glob("*.pdf"))
    return pdfs[:limit]


def main():
    rows = []

    # -------- Invoices --------
    invoice_files = collect_files(INVOICE_DIR, MAX_INVOICES)
    print(f"Processing {len(invoice_files)} invoice PDFs")

    for pdf in invoice_files:
        text = extract_text_from_pdf(pdf)
        if len(text.strip()) < 15:
            continue
        rows.append({
            "text": text.replace("\n", " ").strip(),
            "label": "invoice"
        })

    # -------- Non-Invoices --------
    non_invoice_files = collect_files(NON_INVOICE_DIR, MAX_NON_INVOICES)
    print(f"Processing {len(non_invoice_files)} non-invoice PDFs")

    for pdf in non_invoice_files:
        text = extract_text_from_pdf(pdf)
        if len(text.strip()) < 15:
            continue
        rows.append({
            "text": text.replace("\n", " ").strip(),
            "label": "non-invoice"
        })

    # -------- Write CSV --------
    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Dataset created: {OUTPUT_CSV}")
    print(f"Total samples: {len(rows)}")


if __name__ == "__main__":
    main()
