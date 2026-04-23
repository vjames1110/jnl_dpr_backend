from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine

# Import models here
from app.models import user, site, tmt_dpr
from app.routes import auth, sites, tmt_dpr, reports

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="JNL DPR System")

# CORS (Very Important)

# CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://jnl-dpr-backend.onrender.com",
        "https://jnldpr.netlify.app/"
    ],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(sites.router)
app.include_router(tmt_dpr.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"message": "JNL DPR System Running"}