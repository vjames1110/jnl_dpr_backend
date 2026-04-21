from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.deps import get_current_user

from app.models.tmt_dpr import TMTDPR
from app.models.site import Site

from app.schemas.tmt_dpr import TMTDPRCreate, TMTDPRResponse

router = APIRouter(prefix="/tmt-dpr", tags=["TMT DPR"])


# PM creates DPR
@router.post("", response_model=TMTDPRResponse)
def create_dpr(
    data: TMTDPRCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    

    # only PM allowed
    if user["role"].lower() != "pm":
        raise HTTPException(status_code=403, detail="Only PM can create DPR")

    # check site belongs to PM
    site = db.query(Site).filter(
        Site.id == data.site_id,
        Site.pm_id == user["user_id"]
    ).first()

    if not site:
        raise HTTPException(status_code=403, detail="You cannot add DPR for this site")

    # serial number per site
    last_sl = (
        db.query(func.max(TMTDPR.sl_no))
        .filter(TMTDPR.site_id == data.site_id)
        .scalar()
    )

    sl_no = (last_sl or 0) + 1

    # calculations
    balance = data.po_qty - data.supplied

    supply_percent = (
        (data.supplied / data.po_qty) * 100
        if data.po_qty else 0
    )

    po_value = data.po_qty * data.rate

    # auto PM remarks
    if supply_percent < 50:
        pm_remarks = "PENDING"
    elif 50 <= supply_percent < 90:
        pm_remarks = "PARTIALLY DELIVERED"
    else:
        pm_remarks = "FULLY DELIVERED"

    dpr = TMTDPR(
        **data.dict(),
        sl_no=sl_no,
        balance=balance,
        supply_percent=supply_percent,
        po_value=po_value,
        pm_remarks=pm_remarks,
        created_by=user["user_id"]
    )

    db.add(dpr)
    db.commit()
    db.refresh(dpr)

    return dpr


# Get DPR
@router.get("")
def get_dpr(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    query = (
        db.query(TMTDPR, Site.site_code, Site.site_name)
        .join(Site, Site.id == TMTDPR.site_id)
    )

    # director sees all
    if user["role"].lower() == "director":
        data = query.all()
    else:
        data = query.filter(
            Site.pm_id == user["user_id"]
        ).all()

    result = []

    for i, (dpr, code, name) in enumerate(data, start=1):

        result.append({
            "serial": i,
            "site_code": code,
            "site_name": name,
            "id": dpr.id,
            "sl_no": dpr.sl_no,
            "po_qty": dpr.po_qty,
            "supplied": dpr.supplied,
            "balance": dpr.balance,
            "pm_remarks": dpr.pm_remarks,
            "pm_comment": dpr.pm_comment,
            "director_remarks": dpr.director_remarks,
            "rate": dpr.rate,
            "po_value": dpr.po_value,
            "supply_percent": dpr.supply_percent
        })

    return result

# Director Remarks

@router.put("/director-remarks/{dpr_id}")
def update_director_remarks(
    dpr_id: int,
    remarks: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    if user["role"].lower() != "director":
        raise HTTPException(status_code=403, detail="Only director allowed")

    dpr = db.query(TMTDPR).filter(TMTDPR.id == dpr_id).first()

    if not dpr:
        raise HTTPException(status_code=404, detail="DPR not found")

    dpr.director_remarks = remarks

    db.commit()

    return {"message": "Director remarks updated"}