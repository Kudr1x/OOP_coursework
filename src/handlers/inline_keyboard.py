from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

CALLBACK_PREFIX = "choice_"
choices = ["GPT-4o", "Gemini", "Mistral AI", "GigaChat"]

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

def create_cancel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Завершить", callback_data="cancel"))
    return builder.as_markup()