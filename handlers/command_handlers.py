import os

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from classes import ai_client
from fsm.states import ChatGPTStates, CelebrityDialog
from keyboards import ikb_celebrity, kb_back, kb_start, kb_random_facts

command_router = Router()


@command_router.message(Command('start'))
async def com_start(message: Message):
    await message.answer_photo(
        photo=FSInputFile(path=os.path.join('images', 'main.jpg')),
        caption=f'Привет, {message.from_user.full_name}!\n\nВыберите пункт меню...',
        reply_markup=kb_start(),
    )


@command_router.message(F.text == 'Рандомный факт 🧠')
@command_router.message(F.text == 'Хочу ещё факт 🧠')
@command_router.message(Command('random'))
async def ai_random_fact(message: Message):
    # Имитация "Бот печатает..."
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING
    )
    request_message = [{'role': 'user', 'content': 'Напиши рандомный факт'}]
    caption = await ai_client.text_request(request_message, 'random.txt')
    photo_file = FSInputFile(path=os.path.join('images', 'random.jpg'))
    await message.answer_photo(
        photo=photo_file,
        caption=caption,
        reply_markup=kb_random_facts()
    )


@command_router.message(F.text == 'Задать вопрос ChatGPT 🖥️')
@command_router.message(Command('gpt'))
async def ai_gpt_command(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join('images', 'gpt.jpg'))
    await message.answer_photo(
        photo=photo_file,
        caption='Напишите ваш запрос к ChatGPT',
        reply_markup=kb_back()
    )
    await state.set_state(ChatGPTStates.wait_for_request)


@command_router.message(F.text == 'Диалог с личностью 👤')
@command_router.message(Command('talk'))
async def talk_command(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join('images', 'talk.jpg'))
    await message.answer_photo(
        photo=photo_file,
        caption='Выберите персону для диалога:',
        reply_markup=ikb_celebrity()
    )
    await state.set_state(CelebrityDialog.wait_for_request)

# @command_router.message(Command('help'))
# async def com_help(message: Message):
#     await message.answer(text=f'Привет, {message.from_user.full_name}!')
