from aiogram.filters.callback_data import CallbackData


class CelebrityData(CallbackData, prefix='CD'):
    button: str
    name: str
    file_name: str


class QuizData(CallbackData, prefix='QD'):
    button: str
    theme: str
