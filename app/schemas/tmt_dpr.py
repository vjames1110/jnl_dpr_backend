from pydantic import BaseModel
from datetime import date
from typing import Optional


class TMTDPRCreate(BaseModel):
    site_id: int

    dia_mm: str
    indent_date: date
    indent_qty: float

    po_number: str
    po_date: date

    vendor_name: str
    make: str

    po_qty: float
    today_dispatched: float
    supplied: float

    rate: float

    payment_status: str

    dispatch_start: date
    tentative_completion: date

    qc_cleared: str

    pm_comment: Optional[str] = None


class TMTDPRResponse(BaseModel):
    id: int
    site_id: int
    sl_no: int

    dia_mm: str
    indent_date: date
    indent_qty: float

    po_number: str
    po_date: date

    vendor_name: str
    make: str

    po_qty: float
    today_dispatched: float
    supplied: float

    balance: float
    supply_percent: float
    po_value: float

    pm_remarks: str
    pm_comment: Optional[str]

    director_remarks: Optional[str]

    rate: float
    payment_status: str

    dispatch_start: date
    tentative_completion: date

    qc_cleared: str

    class Config:
        from_attributes = True