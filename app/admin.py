from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from .db import SessionLocal
from .models import Channel, File

router = APIRouter()
templates = Jinja2Templates("app/templates")

@router.get("/")
def dashboard(request: Request):
    db = SessionLocal()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "channels": db.query(Channel).all()
    })

@router.post("/add-channel")
def add_channel(username: str = Form(...)):
    db = SessionLocal()
    db.add(Channel(username=username.replace("@","")))
    db.commit()
    return RedirectResponse("/", 302)

@router.post("/set-file")
def set_file(file_id: str = Form(...)):
    db = SessionLocal()
    db.query(File).delete()
    db.add(File(file_id=file_id))
    db.commit()
    return RedirectResponse("/", 302)
