from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from models import User
from database import get_db
from utils import verify_password

router = APIRouter()

@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "redirect": "/dashboard"}
