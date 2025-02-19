from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_start():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Рандомный факт 🧠')
    keyboard.button(text='Диалог с личностью 👤')
    keyboard.button(text='QUIZ ❓')
    keyboard.button(text='Задать вопрос ChatGPT 🖥️')
    keyboard.adjust(3, 1)
    return keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню...'
    )


def kb_back():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Назад 🔙')
    return keyboard.as_markup(resize_keyboard=True)

def kb_random_facts():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Хочу ещё факт 🧠')
    keyboard.button(text='Закончить 🛑')
    return keyboard.as_markup(resize_keyboard=True)
