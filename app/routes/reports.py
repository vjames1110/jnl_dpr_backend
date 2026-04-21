from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user

from app.services.report_service import (
    get_tmt_reports,
    format_for_excel
)

from app.utils.excel_export import generate_tmt_excel

router = APIRouter(prefix="/reports", tags=["Reports"])



@router.get("/excel")
def export_excel(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    role = current_user.get("role", "").lower()
    user_site = current_user.get("site_code", None)

    data = get_tmt_reports(db, role, user_site)
    excel_data = format_for_excel(data)

    file_stream = generate_tmt_excel(excel_data)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=TMT_DPR_Report.xlsx"
        }
    )