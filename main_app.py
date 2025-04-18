import os
import random
import string
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import db

import replies
import botstates
import keyboards
from ai.yandex_ai import Psychologist, Analyzer

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
admin_chat_id = os.getenv("ADMIN_CHAT_ID")
if not BOT_TOKEN:
    raise ValueError("Токен не найден! Проверьте .env файл.")

from create_bot import bot, dp

psycho_ai = Psychologist()
ai = Analyzer("Ты — помощник по выбору вуза. Помоги с выбором специальности")

db.init_db()

TRANS = {
    "russian": "Русский язык",
    "literature": "Литература",
    "profmat": "Математика профиль",
    "basemat": "Математика базовая",
    "chem": "Химия",
    "geo": "География",
    "obsh": "Обществознание",
    "inf": "Информатика",
    "history": "История",
    "phys": "Физика",
    "bio": "Биология",
    "foreign": "Иностранный язык"
}

#start
@dp.message(Command("start"))
async def send_welcome(message: types.Message, state: FSMContext):
    first_name = message.from_user.first_name
    await message.answer("Привет! Я — твой помощник в выборе вуза и подготовке к экзаменам. Давай начнём с короткой анкеты, чтобы я понял, как тебе помочь! 🎓\n\n Какие предметы ты сдаёшь? Когда выберешь, нажми 'Я выбрал'", reply_markup=keyboards.create_subjects())
    db.register_user(int(message.chat.id), first_name)
    await state.set_state(botstates.RegistrationStates.waiting_for_subjects)

# get user in db
@dp.message(lambda message: message.contact is not None)
async def handle_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    username = message.from_user.username if message.from_user.username else contact.phone_number
    first_name = contact.first_name
    second_name = contact.last_name if contact.last_name else ""
    await state.update_data(
        username=username,
        first_name=first_name,
        second_name=second_name,
        phone_num=contact.phone_number,
        userid=int(message.chat.id)
    )
    await message.answer("Спасибо! Какие предметы ты сдаёшь? Когда выберешь, нажми 'Я выбрал' ❓", reply_markup=keyboards.subjects)
    db.register_user(int(message.chat.id), first_name)
    await state.set_state(botstates.RegistrationStates.waiting_for_subjects)

@dp.callback_query(botstates.RegistrationStates.waiting_for_subjects)
async def process_subjects(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    data_got = await state.get_data()
    data_got["userid"] = callback_query.from_user.id
    if "subjects" not in data_got:
        data_got["subjects"] = []
    if data == 'yes':
        return await callback_query.answer("Уже выбрано!")
    if data != "done":
        if data in data_got["subjects"]:
            return
        data_got["subjects"].append(data)
        await callback_query.answer(f"Вы выбрали: {TRANS[data]}")
        await callback_query.message.edit_text("Привет! Я — твой помощник в выборе вуза и подготовке к экзаменам. Давай начнём с короткой анкеты, чтобы я понял, как тебе помочь! 🎓\n\n Какие предметы ты сдаёшь? Когда выберешь, нажми 'Я выбрал'", reply_markup=keyboards.create_subjects(data_got["subjects"]))
    await state.update_data(data_got)
    if data=="done":
        db.register_subjects(data_got["userid"], data_got["subjects"])
        await callback_query.message.answer(f"Молодец! Пора приступать к подготовке", reply_markup=keyboards.main_menu_keyboard)
        await state.set_state(botstates.MainMenuStates.main)

@dp.message(lambda message: message.text in ["Психолог👩🏻‍⚕️", "Аккаунт💳", "Помощь с выбором специальности✅"])
async def main_menu(message: types.Message, state: FSMContext):
    if message.text == "Психолог👩🏻‍⚕️":
        await message.answer("Опиши свою проблему и ИИ-ассистент окажет тебе моральную поддержку. Чтобы завершить сеанс психотерапии, напиши /stop")
        await state.set_state(botstates.MainMenuStates.psycho)

    if message.text == "Помощь с выбором специальности✅":
        await message.answer("Чтобы мы смогли тебе подобрать специальность, нам нужно, чтобы ты ответил на некоторые вопросы")
        await message.answer("Какая карьерная траектория вас больше привлекает?")
        await state.set_state(botstates.Choice.q1)
    if message.text == "Аккаунт💳":
        await message.answer(f"""
        🆔Ваш id telegram: {message.chat.id}
⭐️Информация о подписке:
 ├ Тип: Pro
 ├ Подписка оформлена: 2025-04-18
 ├ Действует до: 2025-05-18
 ├ Куплена по цене: 0⭐️/месяц
 └ Акция: Применялась
        """)

    if message.text in ["Тренажёры🔒", "Помощь с составлением расписания🔒", "Помощь с расписанием🔒"]:
        await message.answer("Ещё в разработке✅")

@dp.message(botstates.Choice.q1)  # Используем message вместо callback_query
async def choice1(message: types.Message, state: FSMContext):
    data_got = await state.get_data()
    data_got["q1"] = message.text
    await message.answer("К чему у вас были способности в школе? Если затрудняетесь ответить, вспомните слова окружающих или предположите.")
    await state.update_data(data_got)
    await state.set_state(botstates.Choice.q2)

@dp.message(botstates.Choice.q2)  # Используем message вместо callback_query
async def choice2(message: types.Message, state: FSMContext):
    data_got = await state.get_data()
    data_got["q2"] = message.text
    await message.answer("В каких сферах у вас есть практический опыт, о котором приятно вспомнить?")
    await state.update_data(data_got)
    await state.set_state(botstates.Choice.q3)

@dp.message(botstates.Choice.q3)  # Используем message вместо callback_query
async def choice3(message: types.Message, state: FSMContext):
    data_got = await state.get_data()
    data_got["q3"] = message.text
    await message.answer("Подожди, когда ИИ подберет тебе специальности мечты!")
    await state.update_data(data_got)
    await state.set_state(botstates.Choice.AskAI)
    await askainow(message, state)  # Явно вызываем следующую функцию

@dp.message(botstates.Choice.AskAI)
async def askainow(message: types.Message, state:FSMContext):
    data_got = await state.get_data()
    data_got["q3"] = message.text
    a1 = data_got["q1"]
    a2 = data_got["q2"]
    a3 = data_got["q3"]
    got = f"""
    Какая карьерная траектория вас больше привлекает?
    Ответ: {a1}
    К чему у вас были способности в школе? Если затрудняетесь ответить, вспомните слова окружающих или предположите.
    Ответ: {a2}
    В каких сферах у вас есть практический опыт, о котором приятно вспомнить?
    Ответ: {a3}
    """ 
    answer = ai.question(got)

    await message.answer(answer)
    await message.answer("Если у тебя будет вопросы по этой теме, задай их психологу", reply_markup=keyboards.main_menu_keyboard)
    await state.set_state(botstates.MainMenuStates.main)


@dp.message(botstates.MainMenuStates.psycho)  # Используем message вместо callback_query
async def psycho(message: types.Message, state: FSMContext):
    if message.text == "/stop":
        await message.answer("Сеанс закончен", reply_markup=keyboards.main_menu_keyboard)
        await state.set_state(botstates.MainMenuStates.main)
    else:
        try:
            await message.answer(psycho_ai.user_ask(message.text))
        except:
            await message.answer("Ваш запрос не прошёл цензуру, простите")



# back worjk
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
