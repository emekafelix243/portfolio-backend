from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import database
import models
import schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Okeke Felix Emeka - Portfolio API",
    version="1.0.0"
)

# Explicit CORS origins configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://portfolio-frontend-55d.pages.dev",  # Live Cloudflare Pages frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "online", "system": "DeltaQuant Platform Engine"}

@app.post("/api/contact", response_model=schemas.ContactResponse, status_code=status.HTTP_201_CREATED)
def submit_contact_form(payload: schemas.ContactCreate, db: Session = Depends(database.get_db)):
    db_message = models.ContactMessage(**payload.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# Endpoint to fetch form submissions directly via /docs
@app.get("/api/messages", response_model=List[schemas.ContactResponse])
def get_contact_messages(db: Session = Depends(database.get_db)):
    messages = db.query(models.ContactMessage).order_by(models.ContactMessage.id.desc()).all()
    return messages