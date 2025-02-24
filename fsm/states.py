from aiogram.fsm.state import State, StatesGroup


class ChatGPTStates(StatesGroup):
    wait_for_request = State()


class CelebrityDialog(StatesGroup):
    wait_for_answer = State()
    wait_for_request = State()


class QuizGame(StatesGroup):
    wait_for_request = State()
    wait_for_answer = State()
    quiz_next_step = State()
