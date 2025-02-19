from aiogram.fsm.state import State, StatesGroup


class FSMStates(StatesGroup):
    wait_for_request = State()
