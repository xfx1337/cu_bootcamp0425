from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    waiting_for_subjects = State()
    waiting_for_fears = State()

class MainMenuStates(StatesGroup):
    main = State()
    psycho = State()

class Choice(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    AskAI = State()