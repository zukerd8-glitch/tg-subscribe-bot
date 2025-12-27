import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from .db import Base, engine, SessionLocal
from .bot import handle_get_file
from .admin import router as admin_router

Base.metadata.create_all(bind=engine)

bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher()
app = FastAPI()
app.include_router(admin_router, prefix="/admin")

@dp.message()
async def all_messages(message):
    if message.text in ("/start", "Получить файл"):
        db = SessionLocal()
        await handle_get_file(message, bot, db)

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    update = Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}
