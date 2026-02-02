from pydantic import BaseModel
from typing import Optional, Dict, Any, Union


class InvoiceResponse(BaseModel):
    document_type: str
    invoice_number: Optional[str]
    vendor_name: Optional[str]
    invoice_date: Optional[str]
    total_amount: Optional[str]
    customer_name: Optional[str]
    order_id: Optional[str]
    ship_mode: Optional[str]

class NonInvoiceResponse(BaseModel):
    document_type: str

DocumentResponse = Union[InvoiceResponse, NonInvoiceResponse]

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
