from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.api.routes import auth, users
import app.models.user  # noqa: F401 — ensures models are registered before table creation
import app.models.document
from app.api.routes import documents
from app.api.routes import query
import app.models.audit_log
from app.api.routes import audit_logs

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "https://YOUR-FRONTEND.vercel.app"
]

app = FastAPI(
    title="AI Policy & Compliance Checker",
    description="Upload company policies and query them for compliance answers using AI.",
    version="1.0.0",
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(query.router, prefix="/api/v1")
app.include_router(audit_logs.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Compliance Checker API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}