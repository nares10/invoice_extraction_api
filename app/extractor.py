import re
from typing import Dict, Optional


def extract_invoice_data(text: str) -> Dict[str, Optional[str]]:
    data = {}

    # Invoice Number
    match = re.search(r"#\s*(\d+)", text)
    data["invoice_number"] = match.group(1) if match else None

    # Vendor Name (top of document)
    vendor = re.search(r"INVOICE\s*\n#.*\n([A-Za-z0-9 ]+)", text)
    data["vendor_name"] = vendor.group(1).strip() if vendor else None

    # Invoice Date
    date_pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}\s+\d{4}"
    date = re.search(date_pattern, text)
    data["invoice_date"] = date.group(0) if date else None

    # Total Amount
    total = re.search(r"Total\s*:?\s*\$([\d,]+\.\d{2})", text)
    if total:
        data["total_amount"] = total.group(1)
    else:
        amounts = re.findall(r"\$([\d,]+\.\d{2})", text)
        data["total_amount"] = amounts[-1] if amounts else None

    # Customer Name
    bill_to = re.search(r"Bill To\s*:?\s*([A-Za-z ]+)", text)
    data["customer_name"] = bill_to.group(1).strip() if bill_to else None

    # Order ID
    order = re.search(r"Order ID\s*:?\s*([A-Z0-9\-]+)", text)
    data["order_id"] = order.group(1) if order else None

    # Ship Mode
    ship = re.search(r"(First Class|Second Class|Standard Class|Same Day)", text)
    data["ship_mode"] = ship.group(1) if ship else None

    return data