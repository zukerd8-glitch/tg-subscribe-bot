from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

# ===== Настройки =====
BOT_TOKEN = "8265256708:AAHm_ECzLg3_xJIn_8sqjIqUN6TgBmSFycE"  # сюда твой токен
ADMINS = [8364140774]  # сюда твой Telegram ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ===== Хранилище данных =====
channels = []  # список каналов для проверки подписки
files = []     # список file_id для выдачи

# ===== Состояния для FSM =====
class AddFileState(StatesGroup):
    waiting_file = State()

# ===== Админские команды =====
@dp.message(Command(commands=["addchannel"]))
async def add_channel(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Только админ может использовать эту команду")
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Используй: /addchannel channel_username")
        return
    channel = args[1].strip().replace("@", "")
    if channel not in channels:
        channels.append(channel)
        await message.answer(f"✅ Канал {channel} добавлен!")
    else:
        await message.answer("Канал уже добавлен!")

@dp.message(Command(commands=["list"]))
async def list_channels_files(message: Message):
    if message.from_user.id not in ADMINS:
        return
    text = "📦 Каналы:\n"
    text += "\n".join(f"- {c}" for c in channels) if channels else "Нет каналов"
    text += "\n\n📄 Файлы:\n"
    text += "\n".join(f"- {f}" for f in files) if files else "Нет файлов"
    await message.answer(text)

@dp.message(Command(commands=["addfile"]))
async def add_file_start(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Только админ может использовать эту команду")
        return
    await message.answer("Отправь файл в ответ на это сообщение")
    await state.set_state(AddFileState.waiting_file)

@dp.message(AddFileState.waiting_file, content_types=types.ContentType.DOCUMENT)
async def add_file_receive(message: Message, state: FSMContext):
    file_id = message.document.file_id
    if file_id not in files:
        files.append(file_id)
        await message.answer(f"✅ Файл добавлен! file_id: {file_id}")
    else:
        await message.answer("Файл уже добавлен")
    await state.clear()

# ===== Проверка подписки и выдача файлов =====
@dp.message(Command(commands=["start"]))
async def start_command(message: Message):
    if not channels or not files:
        await message.answer("Бот ещё не настроен админом")
        return

    # проверка подписки
    for channel in channels:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=message.from_user.id)
            if member.status not in ["left", "kicked"]:
                # подписан
                await message.answer_document(files[0])
                return
        except Exception as e:
            print(f"Ошибка проверки канала {channel}: {e}")

    await message.answer("❗ Чтобы получить файл, подпишись на все каналы.")

# ===== Запуск бота =====
if __name__ == "__main__":
    import asyncio
    from aiogram import F

    async def main():
        print("Бот запущен")
        await dp.start_polling(bot)

    asyncio.run(main())
