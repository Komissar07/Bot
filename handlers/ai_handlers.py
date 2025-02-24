import os

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from classes import ai_client
from fsm.states import CelebrityDialog, ChatGPTStates, QuizGame
from keyboards import ikb_next_quiz, kb_goodbye, kb_start
from keyboards.callback_data import QuizData

from .command_handlers import quiz_command, talk_command
from .keyboards_handlers import key_stop

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
        message_list = [
            {'role': 'user',
             'content': request}
        ]
        photo_file = FSInputFile(path=os.path.join('images', 'gpt.jpg'))
        caption = await ai_client.text_request(message_list, 'gpt.txt')
        await message.answer_photo(
            photo=photo_file,
            caption=caption,
            reply_markup=kb_start()
        )
    await state.clear()


# Защита от дурака. Заставляет пользоваться кнопками.
# Если пользователь пытается что-то напечатать вместо выбора персоны для диалога.
@ai_router.message(CelebrityDialog.wait_for_request)
async def talk_request(message: Message, state: FSMContext):
    await state.clear()
    await talk_command(message, state)


# Защита от дурака. Заставляет пользоваться кнопками.
# Если пользователь пытается что-то напечатать вместо выбора темы квиза.
@ai_router.message(QuizGame.wait_for_request)
async def quiz_request(message: Message, state: FSMContext):
    await state.clear()
    await quiz_command(message, state)


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


@ai_router.callback_query(QuizData.filter(F.button == 'select_quiz' and F.theme != 'quiz_back'))
async def quiz_get_question(callback: CallbackQuery, callback_data: QuizData, state: FSMContext):
    data = await state.get_data()
    data['score'] = data.get('score', 0)
    if callback_data.theme != 'quiz_more':
        data['type'] = callback_data.theme
    message_list = [
        {'role': 'user',
         'content': data['type']}
    ]
    ai_question = await ai_client.text_request(message_list, 'quiz.txt')
    photo_file = FSInputFile(path=os.path.join('images', 'quiz.jpg'))
    data['question'] = ai_question
    await state.update_data(data)
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo_file,
        caption=ai_question,
    )
    await state.set_state(QuizGame.wait_for_answer)


@ai_router.message(QuizGame.wait_for_answer)
async def quiz_correct_answer(message: Message, state: FSMContext):
    # Имитация "Бот печатает..."
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING
    )
    data = await state.get_data()
    user_answer = message.text
    message_list = [
        {'role': 'assistant', 'content': data['question']},
        {'role': 'user', 'content': user_answer}
    ]
    photo_file = FSInputFile(path=os.path.join('images', 'quiz.jpg'))
    ai_answer = await ai_client.text_request(message_list, 'quiz.txt')
    correct_answer = ai_answer.split(' ', 1)[0]
    if correct_answer == 'Правильно!':
        data['score'] += 1
        await state.update_data(score=data['score'])
    await message.answer_photo(
        photo=photo_file,
        caption=ai_answer + f'\nВаш текущий счёт: {data['score']}',
        reply_markup=ikb_next_quiz()
    )
    await state.set_state(QuizGame.quiz_next_step)
