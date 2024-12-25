import asyncio
from html import unescape

import g4f.models
from aiogram import Router, types, flags
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from g4f import Client

from src.bot.bot_instance import bot
from src.handlers.handler import Handler
from src.keyboard.inline_keyboard import InlineKeyboard
from src.services.gpt_services import chatBot
from src.bot.state import Form

gpts = [g4f.models.gpt_4o, g4f.models.gemini_pro, g4f.models.mistral_large,
        g4f.models.o1_mini, g4f.models.claude_3_5_sonnet]

class MessageHandler(Handler):
    router = Router()

    def __init__(self):
        self.inline_keyboard = InlineKeyboard()

    @staticmethod
    @router.message(CommandStart())
    async def start(message: types.Message, state: FSMContext):
        await state.set_state(Form.choice)

        data = await state.get_data()
        if "selected_choice" not in data:
            await state.update_data(
                client=Client(),
                selected_choice=2
            )
        inline_keyboard = InlineKeyboard()
        reply_markup = await inline_keyboard.create_inline_keyboard_choices_ai(state)
        await message.answer(
            'Привет я бот! Задай свой вопрос и я постараюсь на него ответить',
            reply_markup=reply_markup,
        )

    @staticmethod
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
        inline_keyboard = InlineKeyboard()

        if choise == 5:
            response = await cb.get_image_response(message.text, client)
            if isinstance(response, str):
                await message.answer_photo(
                    response,
                    reply_markup=inline_keyboard.create_image_keyboard()
                )
            else:
                await message.answer("Failed to generate image response.")
        else:
            response, context = cb.get_text_response(message.text, client, current_model=gpts[choise], context=context)

            await state.update_data(context=context)

            unescaped_response = unescape(response)

            await message.answer(
                unescaped_response,
                reply_markup=inline_keyboard.create_text_keyboard(),
            )

