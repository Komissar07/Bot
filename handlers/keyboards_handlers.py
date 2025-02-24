import os

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from keyboards import kb_start
from keyboards.callback_data import CelebrityData, QuizData

keyboard_router = Router()


# @keyboard_router.message(F.text == 'Назад 🔙')
# @keyboard_router.message(F.text == 'Закончить 🛑')
# @keyboard_router.message(F.text == 'Попрощаться 👋')
@keyboard_router.message(F.text)
async def key_stop(message: Message):
    await message.answer_photo(
        photo=FSInputFile(path=os.path.join('images', 'main.jpg')),
        caption='Выберите пункт меню...',
        reply_markup=kb_start(),
    )


@keyboard_router.callback_query(QuizData.filter(F.theme == 'quiz_back'))
@keyboard_router.callback_query(CelebrityData.filter(F.button == '🔙 Назад 🔙'))
async def key_stop_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=FSInputFile(path=os.path.join('images', 'main.jpg')),
        caption='Выберите пункт меню...',
        reply_markup=kb_start(),
    )
