from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from datetime import datetime

from app.core.database import Base


class TMTDPR(Base):
    __tablename__ = "tmt_dpr"

    id = Column(Integer, primary_key=True, index=True)

    # site mapping
    site_id = Column(Integer, ForeignKey("sites.id"))

    # auto serial per site
    sl_no = Column(Integer)

    dia_mm = Column(String)

    indent_date = Column(Date)

    indent_qty = Column(Float)

    po_number = Column(String)

    po_date = Column(Date)

    vendor_name = Column(String)

    make = Column(String)

    po_qty = Column(Float)

    today_dispatched = Column(Float)

    supplied = Column(Float)

    # calculated
    balance = Column(Float)

    supply_percent = Column(Float)

    po_value = Column(Float)

    # auto PM remark
    pm_remarks = Column(String)

    # manual PM comment
    pm_comment = Column(String)

    # director remark
    director_remarks = Column(String)

    rate = Column(Float)

    payment_status = Column(String)

    dispatch_start = Column(Date)

    tentative_completion = Column(Date)

    qc_cleared = Column(String)

    created_by = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)