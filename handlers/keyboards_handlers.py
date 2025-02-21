from aiogram import F, Router
from aiogram.types import Message

from keyboards import kb_start

keyboard_router = Router()


# @keyboard_router.message(F.text == 'Назад 🔙')
# @keyboard_router.message(F.text == 'Закончить 🛑')
# @keyboard_router.message(F.text == 'Попрощаться 👋')
@keyboard_router.message(F.text)
async def key_stop(message: Message):
    await message.answer(
        text='Выберите пункт меню...',
        reply_markup=kb_start()
    )
