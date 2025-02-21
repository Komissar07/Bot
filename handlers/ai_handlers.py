import os

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from classes import ai_client
from fsm.states import ChatGPTStates, CelebrityDialog
from keyboards import kb_start, kb_goodbye

from .keyboards_handlers import key_stop
from .command_handlers import talk_command

ai_router = Router()


@ai_router.message(ChatGPTStates.wait_for_request)
async def ai_gpt_request(message: Message, state: FSMContext):
    if message.text == 'Назад 🔙':
        await key_stop(message)
    else:
        # Имитация "Бот печатает..."
        await message.bot.send_chat_action(
            chat_id=message.from_user.id,
            action=ChatAction.TYPING
        )
        request = message.text
        message_list = [{'role': 'user', 'content': request}]
        photo_file = FSInputFile(path=os.path.join('images', 'gpt.jpg'))
        caption = await ai_client.text_request(message_list, 'gpt.txt')
        await message.answer_photo(
            photo=photo_file,
            caption=caption,
            reply_markup=kb_start()
        )
    await state.clear()


@ai_router.message(CelebrityDialog.wait_for_request)
async def talk_request(message: Message, state: FSMContext):
    await state.clear()
    await talk_command(message, state)


@ai_router.message(CelebrityDialog.wait_for_answer)
async def celebrity_answer(message: Message, state: FSMContext):
    if message.text == 'Назад 🔙':
        await state.clear()
        await key_stop(message)
    else:
        # Имитация "Бот печатает..."
        await message.bot.send_chat_action(
            chat_id=message.from_user.id,
            action=ChatAction.TYPING
        )
        user_text = 'Спасибо за общение! Пока!' if message.text == 'Попрощаться 👋' else message.text
        data = await state.get_data()
        user_request = {
            'role': 'user',
            'content': user_text
        }
        data['dialog'].append(user_request)
        celebrity_response = await ai_client.text_request(data['dialog'], data['prompt'] + '.txt')
        celebrity_response_dict = {
            'role': 'assistant',
            'content': celebrity_response
        }
        data['dialog'].append(celebrity_response_dict)
        photo_file = FSInputFile(path=os.path.join('images', data['prompt'] + '.jpg'))
        await state.update_data(dialog=data['dialog'])
        await message.answer_photo(
            photo=photo_file,
            caption=celebrity_response,
            reply_markup=kb_goodbye()
        )
        if message.text == 'Попрощаться 👋':
            await state.clear()
            await key_stop(message)
