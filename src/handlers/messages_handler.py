import asyncio

from aiogram import Router, types, flags
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from g4f import Client

from src.bot.bot_instance import bot
from src.handlers.inline_keyboard import create_inline_keyboard_choices_ai, create_cancel_keyboard
from src.services.gpt_services import get
from src.bot.state import Form


router = Router()


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.set_state(Form.choice)
    await state.update_data(client=Client())
    reply_markup = await create_inline_keyboard_choices_ai(state)
    await message.answer(
        'Привет я бот! Задай свой вопрос и я постараюсь на него ответить',
        reply_markup=reply_markup,
    )

@flags.chat_action("typing")
@router.message()
async def handle_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    client = data.get("client")
    if client is None:
        client = Client()
        await state.update_data(client=client)
    context = data.get("context", [])

    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    await asyncio.sleep(2)

    response, context = get(message.text, client, context)

    await state.update_data(context=context)

    escaped_response = html.escape(response)
    await message.answer(
        escaped_response,
        reply_markup=create_cancel_keyboard(),
    )