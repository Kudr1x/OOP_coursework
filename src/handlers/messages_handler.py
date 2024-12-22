import asyncio
from html import escape, unescape

from aiogram import Router, types, flags
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from g4f import Client

from src.bot.bot_instance import bot
from src.handlers.inline_keyboard import create_inline_keyboard_choices_ai, create_cancel_keyboard
from src.services.gpt_services import chatBot
from src.bot.state import Form


router = Router()

GET_PREFIX = "g4f.models."
GPT_MODELS = ["gpt_4o", "gemini", "mistral_large", "gigachat"]

@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.set_state(Form.choice)

    data = await state.get_data()
    if "selected_choice" not in data:
        await state.update_data(
            client=Client(),
            selected_choice=2
        )

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
    choise = data.get("selected_choice", 2)

    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    await asyncio.sleep(3)

    cb = chatBot()
    print(GET_PREFIX+GPT_MODELS[choise])
    response, context = cb.get_response(message.text, client, current_model=GET_PREFIX+GPT_MODELS[choise], context=context)

    await state.update_data(context=context)

    unescaped_response = unescape(response)
    await message.answer(
        unescaped_response,
        reply_markup=create_cancel_keyboard(),
    )