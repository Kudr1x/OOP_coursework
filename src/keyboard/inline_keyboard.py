from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

CALLBACK_PREFIX = "choice_"
choices = ["GPT-4o", "Gemini Pro", "Mistral AI", "o1-mini", "Claude AI", "Генерация фото"]

class InlineKeyboard:
    def __init__(self):
        pass

    @staticmethod
    async def create_inline_keyboard_choices_ai(state: FSMContext):
        data = await state.get_data()
        selected_choice = data.get("selected_choice")
        builder = InlineKeyboardBuilder()
        row = []
        for i, choice in enumerate(choices):
            text = choice
            if selected_choice == i:
                text += " ✅"
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=f"{CALLBACK_PREFIX}{i}")
            )
            if len(row) == 2:
                builder.row(*row)
                row = []
        if row:
            builder.row(*row)
        return builder.as_markup()


    @staticmethod
    def create_text_keyboard():
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="❌ Завершить", callback_data="cancel"),
            InlineKeyboardButton(text="✍️ Продолжить", callback_data="continue")
        )
        builder.row(
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")
        )
        return builder.as_markup()

    @staticmethod
    def create_image_keyboard():
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="❌ Завершить", callback_data="cancel"),
            InlineKeyboardButton(text="🖼 Повторить", callback_data="repeat")
        )
        builder.row(
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")
        )
        return builder.as_markup()