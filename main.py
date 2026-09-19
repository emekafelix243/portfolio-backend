from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database
import models
import schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Okeke Felix Emeka - Portfolio API",
    version="1.0.0"
)

# Define allowed origins for CORS
origins = [
    "http://localhost:3000",      # Local Next.js dev server
    "http://127.0.0.1:3000",      # Local alternative host
    "https://*.pages.dev",        # Cloudflare Pages previews
    "*"                           # Wildcard for production fallback
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
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