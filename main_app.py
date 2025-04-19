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

import test_utils
from test_utils import STRESS_WORDS


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
admin_chat_id = os.getenv("ADMIN_CHAT_ID")
if not BOT_TOKEN:
    raise ValueError("Токен не найден! Проверьте .env файл.")

from create_bot import bot, dp
from aiogram import types

psycho_ai = {}
ai = {}
ask_answers = {}
async def create_physicol(user_id):
    global psycho_ai
    if user_id in psycho_ai:
        psycho_ai[user_id].clear()
        return
    psycho_ai[user_id] = Psychologist()
    psycho_ai[user_id] = await psycho_ai[user_id].init()

async def create_ai(user_id):
    global ai
    if user_id in ai:
        ai[user_id].clear()
        return
    ai[user_id] = await Analyzer().init("""Ты — виртуальный консультант по поступлению в вуз. Задавай вопросы по одному, чтобы помочь пользователю определиться с выбором. Следуй схеме:

Профессиональные интересы: «Какую сферу деятельности вы рассматриваете? Например, IT, медицина, инженерия» 
Баллы ЕГЭ: «Какие экзамены вы сдаёте и какой примерный балл ожидаете?» 
Локация: «В каком городе/регионе хотите учиться?»
Бюджет/платное: «Вас интересуют бюджетные места или готовы рассмотреть платное обучение?»
Дополнительно: «Важны ли стипендии, практики»""", memory=True)


db.init_db()

TRANS = {
    "russian": "Русский язык",
    "literature": "Литература",
    "profmat": "Математика проф.",
    "basemat": "Математика база",
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
    if db.check_subjects(message.from_user.id):
        await message.answer(f"Твои возможности:", reply_markup=keyboards.main_menu_keyboard)
        return await state.set_state(botstates.MainMenuStates.main)
    first_name = message.from_user.first_name
    await message.answer("Привет! Я — твой помощник в выборе вуза и подготовке к экзаменам. Давай начнём с короткой анкеты, чтобы я понял, как тебе помочь! 🎓\n\n Какие предметы ты сдаёшь? Когда выберешь, нажми 'Я выбрал'", reply_markup=keyboards.create_subjects())
    db.register_user(int(message.chat.id), first_name)
    await state.set_state(botstates.RegistrationStates.waiting_for_subjects)

@dp.callback_query(lambda call: call.data == "subscription")
async def process_subjects(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer("Сегодня в честь ЭКСПО - подписка бесплатная и её нельзя продлить. Всё ради вас💘", True)

@dp.callback_query(lambda call: call.data == "edit_subjects")
async def process_subjects(callback_query: types.CallbackQuery, state: FSMContext):
    db.delete_subjects(callback_query.from_user.id)
    await callback_query.message.edit_text("Привет! Я — твой помощник в выборе вуза и подготовке к экзаменам. Давай начнём с короткой анкеты, чтобы я понял, как тебе помочь! 🎓\n\n Какие предметы ты сдаёшь? Когда выберешь, нажми 'Я выбрал'", reply_markup=keyboards.create_subjects())
    await state.set_state(botstates.RegistrationStates.waiting_for_subjects)

@dp.callback_query(botstates.RegistrationStates.waiting_for_subjects)
async def process_subjects(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    data_got = await state.get_data()
    data_got["userid"] = callback_query.from_user.id
    if "subjects" not in data_got:
        data_got["subjects"] = []
    if data != "done":
        if data in data_got["subjects"]:
            data_got["subjects"].remove(data)
            await callback_query.answer(f"Вы отменили выбор: {TRANS[data]}")
        else:
            data_got["subjects"].append(data)
            await callback_query.answer(f"Вы выбрали: {TRANS[data]}")
        if data in ["profmat", "basemat"]:
            if data == "profmat" and "basemat" in data_got["subjects"]:
                data_got["subjects"].remove("basemat")
            elif data == "basemat" and "profmat" in data_got["subjects"]:
                data_got["subjects"].remove("profmat")
        await callback_query.message.edit_text("Привет! Я — твой помощник в выборе вуза и подготовке к экзаменам. Давай начнём с короткой анкеты, чтобы я понял, как тебе помочь! 🎓\n\n Какие предметы ты сдаёшь? Когда выберешь, нажми 'Я выбрал'", reply_markup=keyboards.create_subjects(data_got["subjects"]))
    await state.update_data(data_got)
    if data=="done":
        db.register_subjects(data_got["userid"], data_got["subjects"])
        await callback_query.message.answer(f"Молодец! Пора приступать к подготовке", reply_markup=keyboards.main_menu_keyboard)
        await state.set_state(botstates.MainMenuStates.main)
        await callback_query.message.delete()

@dp.message(lambda message: message.text in ["Помощь с расписанием🔒", "Помощь с составлением расписания🔒"])
async def main_menu(message: types.Message, state: FSMContext):
    await message.answer("Функция в разработке. . .")

@dp.message(lambda message: message.text.lower() in ["психолог👩🏻‍⚕️", "аккаунт💳", "помощь с выбором специальности✅", "тренажёры🚀"])
async def main_menu(message: types.Message, state: FSMContext):
    if message.text.lower() == "психолог👩🏻‍⚕️":
        msg = await message.answer("Создание модели...")
        await create_physicol(message.from_user.id)
        await msg.edit_text("Опиши свою проблему и ИИ-ассистент окажет тебе моральную поддержку. Чтобы завершить сеанс психотерапии, напиши /stop")
        await state.set_state(botstates.MainMenuStates.psycho)

    if message.text.lower() == "тренажёры🚀":
        await message.answer("🚀Выберите тренажёр из представленных", reply_markup=keyboards.tests_keyboard)
        await state.set_state(botstates.MainMenuStates.tests)

    if message.text.lower() == "помощь с выбором специальности✅":
        await message.answer("""🌟 <b>Приветствуем в подборе специальности!</b> 🌟

Чтобы мы могли подобрать для тебя идеальный вариант, нужно ответить на <b>7 простых вопросов</b>. 

🚀 <b>Как это работает?</b>
1. Отвечай на вопросы максимально честно
2. Не задерживайся слишком долго над ответами
3. Используй кнопки или текстовые ответы

⚠️ <b>Хочешь прервать тест?</b>
- Напиши "Стоп" для полного завершения
- Или "Завершить" для моментального анализа

Все данные обрабатываются анонимно и не сохраняются ✅

Готов начать? Тогда поехали! 🚀""")
        msg = await message.answer("Создание модели. . .")
        await create_ai(message.from_user.id)
        await msg.edit_text("Подбор вопроса. . .")
        try:
            await msg.edit_text(await ai[message.from_user.id].question(f"Человек ответил: {message.text}\nЗадай вопрос ему по инструкции"))
        except Exception as e:
            print(e)
            await msg.edit_text("При генерации вопроса произошла ошибка на стороне YandexGPT")
        await state.set_state(botstates.Choice.q)
    if message.text == "Аккаунт💳":
        subjects_mass = db.get_subjects(message.from_user.id)
        subjects = ""
        for item in subjects_mass:
            subjects += TRANS[item["subject"]] + ", "
        subjects = subjects[:-2]
        await message.answer(f"""
        🆔Ваш id telegram: {message.from_user.id}
⭐️Информация о подписке:
 ├ Тип: Pro
 ├ Подписка оформлена: 19.04.2025
 ├ Действует до: 20.04.2025
 ├ Куплена по цене: 0⭐️/месяц
 └ Акция: Применялась

Выбранные вами предметы: {subjects}
        """, reply_markup=keyboards.profile)

    if message.text in ["Тренажёры🔒", "Помощь с составлением расписания🔒", "Помощь с расписанием🔒"]:
        await message.answer("Ещё в разработке✅")

@dp.message(botstates.MainMenuStates.tests)
async def tests_choice(message: types.Message, state: FSMContext):
    if message.text.lower() == "орфоэпия":
        await state.set_state(botstates.Tests.rus_orfoepia)
        word = test_utils.get_stress_word()
        await message.answer("Напишите слово с правильно поставленным ударением, отметив ударение заглавной буквой: \n\n" + word.lower() 
        + "\n\n Чтобы остановить тренажёр, напишите 'Стоп'")
        await state.update_data(current_word=word)
    else:
        await state.set_state(botstates.MainMenuStates.main)
        await message.answer("Ещё в разработке✅", reply_markup=keyboards.main_menu_keyboard)

@dp.message(botstates.Tests.rus_orfoepia)
async def rus_orfoepia_test(message: types.Message, state: FSMContext):
    data = await state.get_data()
    word = test_utils.get_stress_word()
    if message.text == None:
        cword = data["current_word"]
        await message.answer(f"Неверно! Правильное написание: <b>{cword}</b>\n Следующее слово: <b>" + word.lower() + "</b>")
        return
    if message.text in STRESS_WORDS and message.text.lower() == data["current_word"].lower():
        await message.answer("Верно! \n Следующее слово: " + word.lower())
    elif message.text.lower() == "стоп":
        await state.set_state(botstates.MainMenuStates.main)
        await message.answer("Тестирование окончено", reply_markup=keyboards.main_menu_keyboard)
    else:
        cword = data["current_word"]
        await message.answer(f"Неверно! Правильное написание: {cword}\n Следующее слово: " + word.lower())
    data["current_word"] = word
    await state.update_data(data)
        

@dp.message(botstates.Choice.q)  # Используем message вместо callback_query
async def choice1(message: types.Message, state: FSMContext):
    if message.text.lower() == "стоп":
        await state.set_state(botstates.MainMenuStates.main)
        return await message.answer("Обработка остановлена!")
    if message.text.lower() == "завершить":
        return await askainow(message, state)
    msg = await message.answer("Подбор вопроса. . .")
    if ai[message.from_user.id].message_count >= 6:
        await state.set_state(botstates.Choice.AskAI)
    try:
        await msg.edit_text(await ai[message.from_user.id].question(f"Человек ответил: {message.text}\nЗадай вопрос ему по инструкции"))
    except Exception as e:
        print(e)
        await msg.edit_text("При генерации вопроса произошла ошибка на стороне YandexGPT")


@dp.message(botstates.Choice.AskAI)
async def askainow(message: types.Message, state:FSMContext):
    msg = await message.answer("Анализ ответов...")
    subjects_mass = db.get_subjects(message.from_user.id)
    subjects = ""
    for item in subjects_mass:
        subjects += TRANS[item["subject"]] + ", "
    subjects = subjects[:-2]
    answer = await ai[message.from_user.id].question(f"Человек ответил: {message.text}. Также информация о предметах человека: {subjects}. Всё, выдай результат, какие вузы подходят.",
                               "llama")
    await msg.edit_text(answer)
    await message.answer("Если у тебя будет вопросы по этой теме, задай их психологу", reply_markup=keyboards.main_menu_keyboard)
    await state.set_state(botstates.MainMenuStates.main)


@dp.message(botstates.MainMenuStates.psycho)  # Используем message вместо callback_query
async def psycho(message: types.Message, state: FSMContext):
    if message.text == "/stop":
        await message.answer("Сеанс закончен", reply_markup=keyboards.main_menu_keyboard)
        await state.set_state(botstates.MainMenuStates.main)
    else:
        msg = await message.answer("Обдумываю ваш запрос. . .")
        try:
            await msg.edit_text(await psycho_ai[message.from_user.id].user_ask(message.text))
        except:
            await message.answer("Ваш запрос не прошёл цензуру, простите")




# back worjk
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio

    asyncio.run(main())