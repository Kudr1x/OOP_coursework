from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from src.handlers.handler import Handler
from src.keyboard.inline_keyboard import CALLBACK_PREFIX, InlineKeyboard


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
        await callback_query.message.edit_reply_markup(reply_markup=reply_markup)
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
        pass