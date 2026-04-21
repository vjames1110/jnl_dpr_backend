from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteResponse

router = APIRouter(prefix="/sites", tags=["Sites"])


@router.post("", response_model=SiteResponse)
def create_site(data: SiteCreate, db: Session = Depends(get_db)):
    
    site = Site(**data.dict())

    db.add(site)
    db.commit()
    db.refresh(site)

    return site


@router.get("", response_model=list[SiteResponse])
def get_sites(db: Session = Depends(get_db)):
    
    return db.query(Site).all()

# PM gets only his sites
@router.get("/my-sites")
def get_my_sites(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    if user["role"].lower() == "director":
        sites = db.query(Site).all()
    else:
        sites = db.query(Site).filter(
            Site.pm_id == user["user_id"]
        ).all()

    return [
        {
            "value": s.id,
            "label": f"{s.site_name} ({s.site_code})"
        }
        for s in sites
    ]