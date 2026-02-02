from PyPDF2 import PdfReader
import re
from typing import Dict, Optional

reader = PdfReader("./data/invoices/invoice_Adam Shillingsburg_12471.pdf")
page = reader.pages[0]
text = page.extract_text()

def extract_invoice_data(text: str) -> Dict[str, Optional[str]]:
    data = {}

    # ---------- Invoice Number ----------
    invoice_no = re.search(r"#\s*(\d+)", text)
    data["invoice_number"] = invoice_no.group(1) if invoice_no else None

    # ---------- Vendor Name ----------
    # Usually appears near top after INVOICE
    vendor = re.search(r"INVOICE\s*\n#.*\n([A-Za-z0-9 ]+)", text)
    data["vendor_name"] = vendor.group(1).strip() if vendor else None

    # ---------- Date ----------
    date_pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}\s+\d{4}"
    date_match = re.search(date_pattern, text)
    data["invoice_date"] = date_match.group(0) if date_match else None

    # ---------- Total Amount ----------
    # Prefer "Total" keyword
    total_match = re.search(r"Total\s*:?\s*\$([\d,]+\.\d{2})", text)
    if total_match:
        data["total_amount"] = total_match.group(1)
    else:
        # fallback: last currency value
        amounts = re.findall(r"\$([\d,]+\.\d{2})", text)
        data["total_amount"] = amounts[-1] if amounts else None

    # ---------- Customer Name ----------
    bill_to = re.search(r"Bill To\s*:?\s*([A-Za-z ]+)", text)
    data["customer_name"] = bill_to.group(1).strip() if bill_to else None

    # ---------- Order ID ----------
    order_id = re.search(r"Order ID\s*:?\s*([A-Z0-9\-]+)", text)
    data["order_id"] = order_id.group(1) if order_id else None

    # ---------- Shipping Address ----------
    ship_to = re.search(r"Ship To\s*:?\s*([\w\s,]+)", text)
    data["shipping_address"] = ship_to.group(1).strip() if ship_to else None

    # ---------- Ship Mode ----------
    ship_mode = re.search(r"(First Class|Second Class|Standard Class|Same Day)", text)
    data["ship_mode"] = ship_mode.group(1) if ship_mode else None

    return data

print(extract_invoice_data(text))
