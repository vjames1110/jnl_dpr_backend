from fastapi import FastAPI
from app.core.database import Base, engine

# Import models here
from app.models import user, site, tmt_dpr
from app.routes import auth, sites, tmt_dpr

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="JNL DPR System")

app.include_router(auth.router)
app.include_router(sites.router)
app.include_router(tmt_dpr.router)


@app.get("/")
def root():
    return {"message": "JNL DPR System Running"}