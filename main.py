from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext  # Import Passlib for hashing
from database import engine, get_db
import models

# Initialize FastAPI
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return templates.TemplateResponse("home.html", {"request": request, "users": users})

@app.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    name: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return RedirectResponse(url="/?error=User+Exists", status_code=303)
    
    hashed_password = pwd_context.hash(password)  # Hash password before saving
    new_user = models.User(email=email, name=name, phone=phone, password=hashed_password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/login", status_code=303)

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user or not pwd_context.verify(password, user.password):  # Verify hashed password
        return RedirectResponse(url="/?error=Invalid+credentials", status_code=303)
    
    return RedirectResponse(url=f"/user/{email}", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    error = request.query_params.get("error", "")
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.get("/user/{email}", response_class=HTMLResponse)
async def user_detail(request: Request, email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("user_details.html", {"request": request, "user": user})

@app.get("/dashboard/{email}", response_class=HTMLResponse)
async def dashboard(request: Request, email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})



