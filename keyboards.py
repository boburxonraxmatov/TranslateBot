from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from configs import LANGUAGES


def generate_languages():
    markup = ReplyKeyboardMarkup(row_width=2) # Сколько кнопок будет в 1 строчку
    # markup.add(
    #     KeyboardButton(text='О боте')
    # )
    buttons = []
    for lang in LANGUAGES.values():
        btn = KeyboardButton(text=lang)
        buttons.append(btn)
    markup.add(*buttons)
    return markup


# list1 = [1,2,3]
# print(*list1)