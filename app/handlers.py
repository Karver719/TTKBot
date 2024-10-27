import os
import random
from pathlib import Path
from aiogram.filters import Command
from aiogram import types, Dispatcher, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from stt import STT
from dotenv import load_dotenv
from SQLcom import get_fio_from_admins, get_fio_from_customers, add_tg_id
from func import search, buttons, stop_buttons
import re
from sqlalchemy.orm import sessionmaker
from SQLcom import engine, Customer  # Импортируем engine и Customer из SQLcom.py
from models import Customer

load_dotenv()
TELEGRAM_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
stt = STT()

class Form(StatesGroup):
    fio = State()
    phone = State()
    email = State()

# Хэндлер на команду /start , /help
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f"Здравствуйте введите операцию:\n"
                         f"1. Войти как клиент ТТК\n"
                         f"2. Заключить новый договор")

@dp.message(F.text == "1")
async def start(message: types.Message):
    await message.answer(f"Введите номер договора: 516хххххх:")

@dp.message(F.text == "да")
async def apruv(message: types.Message):
    if search(message.text.lower()):
        await message.answer(f"Хорошо иду в профиль")

@dp.message(F.text == "2")
async def start_form(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше ФИО:")
    await state.set_state(Form.fio)

@dp.message(Form.fio)
async def process_fio(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await message.answer("Введите ваш телефонный номер:")
    await state.set_state(Form.phone)

@dp.message(Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Введите ваш email:")
    await state.set_state(Form.email)

@dp.message(Form.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    user_data = await state.get_data()

    # Генерация номера договора
    contract_number = f"516{random.randint(100000, 999999)}"

    # Добавление в базу данных
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        customer = Customer(
            num_dog=contract_number,
            fio=user_data['fio'],
            telephone=user_data['phone'],
            mail=user_data['email'],
            telegram_id=str(message.from_user.id)
        )
        session.add(customer)
        session.commit()
        await message.answer(f"Ваши данные сохранены. Ваш номер договора: {contract_number}")
    except Exception as e:
        session.rollback()
        await message.answer("Ошибка при сохранении данных.")
    finally:
        session.close()

    await state.clear()

# Хэндлер на получение голосового и аудио сообщения
@dp.message(lambda message: message.content_type in [types.ContentType.VOICE, types.ContentType.AUDIO,
                                                     types.ContentType.DOCUMENT])
async def handle_audio_files(message: types.Message):
    try:
        if message.content_type == types.ContentType.VOICE:
            file_id = message.voice.file_id
        elif message.content_type == types.ContentType.AUDIO:
            file_id = message.audio.file_id
        elif message.content_type == types.ContentType.DOCUMENT:
            file_id = message.document.file_id
        else:
            await message.reply("Формат документа не поддерживается")
            return

        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_on_disk = Path(f"{file_id}.tmp")
        await bot.download_file(file_path, destination=file_on_disk)
        await message.reply("Аудио получено")

        # Проверка, что файл существует
        if not file_on_disk.exists():
            await message.reply("Файл не был сохранен на диск")
            return

        # ====================================================================================
        text = stt.audio_to_text(file_on_disk)
        # ====================================================================================

        if not text:
            await message.answer("Не удалось распознать текст")
            os.remove(file_on_disk)
            return

        os.remove(file_on_disk)
        # Подбор ответов по пойманным словам
        answer = search(text.lower())
        await message.answer(answer)

    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
