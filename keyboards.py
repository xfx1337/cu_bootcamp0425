from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Тренажёры🔒"), KeyboardButton(text="Помощь с составлением расписания🔒")],
        [KeyboardButton(text="Психолог👩🏻‍⚕️"), KeyboardButton(text="Помощь с выбором специальности✅")],
        [KeyboardButton(text="Помощь с расписанием🔒"), KeyboardButton(text="Аккаунт💳")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
def create_subjects(data=[]):
    test = {
        "russian": "Русский язык",
        "literature": "Литература",
        "basemat": "Базовая математика",
        "profmat": "Профильная математика",
        "phys": "Физика",
        "chem": "Химия",
        "bio": "Биология",
        "history": "История",
        "geo": "География",
        "obsh": "Обществознание",
        "foreign": "Иностранный язык",
        "inf": "Информатика",
        "done": "✅ Я выбрал"
    }
    keyboard = []
    for callback, text in test.items():
        if callback in data:
            keyboard.append(InlineKeyboardButton(text="🟢" + text, callback_data='yes'))
        else:
            keyboard.append(InlineKeyboardButton(text=text, callback_data=callback))
    
    keyboard_final = []
    temp = []
    for i in range(len(keyboard)):
        temp.append(keyboard[i])
        if i % 2 == 1:
            keyboard_final.append(temp)
            temp = []
    if temp:
        keyboard_final.append(temp)
    subjects = InlineKeyboardMarkup(
        inline_keyboard=keyboard_final,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return subjects