from pydantic import BaseModel


class SiteCreate(BaseModel):
    site_name: str
    site_code: str
    pm_id: int


class SiteResponse(BaseModel):
    id: int
    site_name: str
    site_code: str
    pm_id: int

    class Config:
        from_attributes = True