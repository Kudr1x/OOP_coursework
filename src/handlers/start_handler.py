import html

from aiogram import Router, types
from aiogram.filters import CommandStart

from src.services.gpt_services import get

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Привет я бот! Задай свой вопрос и я постараюсь на него ответить')

@router.message()
async def handle_message(message: types.Message):
    response = get(message.text)
    escaped_response = html.escape(response)
    await message.answer(escaped_response)