from html import unescape

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from g4f import Client

from src.bot.state import Form
from src.handlers.handler import Handler
from src.handlers.messages_handler import gpts
from src.keyboard.inline_keyboard import CALLBACK_PREFIX, InlineKeyboard
from src.services.gpt_services import chatBot


class CallbackHandler(Handler):
    router = Router()

    def __init__(self):
        self.inline_keyboard = InlineKeyboard()

    @staticmethod
    @router.callback_query(lambda c: c.data.startswith(CALLBACK_PREFIX))
    async def handle_callback_query(callback_query: types.CallbackQuery, state: FSMContext):
        selected_choice = int(callback_query.data[len(CALLBACK_PREFIX):])
        data = await state.get_data()
        current_selected = data.get("selected_choice")

        if current_selected == selected_choice:
            await callback_query.answer()
            return

        await state.update_data(selected_choice=selected_choice)

        inline_keyboard = InlineKeyboard()
        reply_markup = await inline_keyboard.create_inline_keyboard_choices_ai(state)

        if callback_query.message.reply_markup != reply_markup:
            await callback_query.message.edit_reply_markup(reply_markup=reply_markup)

        if selected_choice != 5:
            new_text = "Выбрана нейросеть: " + gpts[selected_choice].name
        else:
            new_text = "Выбрана генерация фото"
        if callback_query.message.text != new_text:
            await callback_query.message.edit_text(new_text)

        await callback_query.answer()

    @staticmethod
    @router.callback_query(lambda c: c.data == "cancel")
    async def cancel_callback(callback_query: types.CallbackQuery, state: FSMContext):
        await state.update_data(context=[])
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer("Чат очищен! Можете задать новый вопрос!")

    @staticmethod
    @router.callback_query(lambda c: c.data == "continue")
    async def cancel_callback(callback_query: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        client = data.get("client")
        if client is None:
            client = Client()
            await state.update_data(client=client)
        context = data.get("context", [])
        choise = data.get("selected_choice", 2)

        cb = chatBot()
        response, context = cb.get_response("Продолжи", client, current_model=gpts[choise], context=context)

        await state.update_data(context=context)

        unescaped_response = unescape(response)
        inline_keyboard = InlineKeyboard()

        await callback_query.message.answer(
            unescaped_response,
            reply_markup=inline_keyboard.create_text_keyboard(),
        )

        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer()

    @staticmethod
    @router.callback_query(lambda c: c.data == "continue")
    async def cancel_callback(callback_query: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        client = data.get("client")
        if client is None:
            client = Client()
            await state.update_data(client=client)
        context = data.get("context", [])
        choise = data.get("selected_choice", 2)

        cb = chatBot()
        response, context = cb.get_text_response("Продолжи", client, current_model=gpts[choise], context=context)

        await state.update_data(context=context)

        unescaped_response = unescape(response)
        inline_keyboard = InlineKeyboard()

        await callback_query.message.answer(
            unescaped_response,
            reply_markup=inline_keyboard.create_text_keyboard(),
        )

        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer()

    @staticmethod
    @router.callback_query(lambda c: c.data == "settings")
    async def cancel_callback(callback_query: types.CallbackQuery, state: FSMContext):
        await state.set_state(Form.choice)

        data = await state.get_data()
        if "selected_choice" not in data:
            await state.update_data(
                client=Client(),
                selected_choice=2
            )

        await callback_query.message.edit_reply_markup(reply_markup=None)

        inline_keyboard = InlineKeyboard()
        reply_markup = await inline_keyboard.create_inline_keyboard_choices_ai(state)
        await callback_query.message.answer(
            'Какую нейросеть выберем?',
            reply_markup=reply_markup,
        )

    @staticmethod
    @router.callback_query(lambda c: c.data == "repeat")
    async def cancel_callback(callback_query: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        client = data.get("client")
        if client is None:
            client = Client()
            await state.update_data(client=client)

        cb = chatBot()
        response = await cb.get_image_response(cb.last_picture_response, client)

        inline_keyboard = InlineKeyboard()

        await callback_query.message.answer_photo(
            response,
            reply_markup=inline_keyboard.create_image_keyboard(),
        )

        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer()