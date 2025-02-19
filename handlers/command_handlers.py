import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from keyboards import kb_start

command_router = Router()


@command_router.message(F.text == 'Назад 🔙')
@command_router.message(F.text == 'Закончить 🛑')
@command_router.message(Command('start'))
async def com_start(message: Message):
    await message.answer_photo(
        photo=FSInputFile(path=os.path.join('images', 'main.jpg')),
        caption=f'Привет, {message.from_user.full_name}!',
        reply_markup=kb_start(),
    )


@command_router.message(Command('help'))
async def com_help(message: Message):
    await message.answer(text=f'Привет, {message.from_user.full_name}!')
