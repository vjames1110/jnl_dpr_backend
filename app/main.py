from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="JNL DPR System")

# CORS FIRST (before routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://jnldpr.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IMPORTS AFTER APP CREATION
from app.routes import auth, sites, tmt_dpr, reports

app.include_router(auth.router)
app.include_router(sites.router)
app.include_router(tmt_dpr.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "JNL DPR System Running"}