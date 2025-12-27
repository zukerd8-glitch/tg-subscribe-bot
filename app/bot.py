from aiogram import Bot, Dispatcher, types
from sqlalchemy.orm import Session
from .models import Channel, File, User

async def handle_get_file(message: types.Message, bot: Bot, db: Session):
    user_id = message.from_user.id

    channels = db.query(Channel).all()
    not_sub = []

    for ch in channels:
        member = await bot.get_chat_member(f"@{ch.username}", user_id)
        if member.status in ("left", "kicked"):
            not_sub.append(ch.username)

    if not_sub:
        text = "Подпишитесь на каналы:\n"
        for ch in not_sub:
            text += f"https://t.me/{ch}\n"
        await message.answer(text)
        return

    file = db.query(File).first()
    if not file:
        await message.answer("Файл не загружен")
        return

    await bot.send_document(message.chat.id, file.file_id)
