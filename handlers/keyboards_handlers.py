from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import kb_back

keyboard_router = Router()


@keyboard_router.message(F.text == 'ChatGPT')
async def kb_chatgpt(message: Message):
    await message.answer(
        text='Здесь будет функционал ChatGPT',
        reply_markup=kb_back()
    )

# @keyboard_router.message(Command('random'))
# @keyboard_router.message(F.text == 'Рандомный факт 🧠')
# async def kb_chatgpt(message: Message):
#     await message.answer(
#         text='Сейчас выдам рандомный факт',
#         reply_markup=kb_back()
#     )
