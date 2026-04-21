from sqlalchemy.orm import Session
from sqlalchemy import join

from app.models.tmt_dpr import TMTDPR
from app.models.site import Site


# =========================
# GET FULL REPORT DATA
# =========================
def get_tmt_reports(db: Session, role: str, user_site: str = None):

    query = db.query(
        TMTDPR,
        Site.site_code,
        Site.site_name
    ).join(Site, TMTDPR.site_id == Site.id)

    # ROLE BASED ACCESS CONTROL
    role = role.lower()

    if role == "pm" and user_site:
        query = query.filter(TMTDPR.site_id == user_site)

    results = query.all()

    return results


# =========================
# FORMAT FOR EXCEL EXPORT
# =========================
def format_for_excel(rows):

    result = []

    for row in rows:

        dpr = row[0]  # TMTDPR object
        site_code = row[1]
        site_name = row[2]

        result.append({
            "serial": dpr.sl_no,
            "site_code": site_code,
            "site_name": site_name,
            "po_qty": dpr.po_qty,
            "supplied": dpr.supplied,
            "balance": dpr.balance,
            "supply_percent": dpr.supply_percent,
            "pm_remarks": dpr.pm_remarks,
            "pm_comment": dpr.pm_comment,
            "director_remarks": dpr.director_remarks
        })

    return result