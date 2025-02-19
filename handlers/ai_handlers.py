import os
import httpx
import aiofiles
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from openai import AsyncOpenAI
from .command_handlers import com_start
from keyboards import kb_random_facts, kb_start, kb_back
from fsm.states import FSMStates

ai_router = Router()

ai_client = AsyncOpenAI(
    api_key=os.getenv('AI_TOKEN'),
    http_client=httpx.AsyncClient(proxy=os.getenv('PROXY'))
)


async def read_prompt(name: str):
    async with aiofiles.open('prompts/' + name, 'r', encoding='UTF-8') as file:
        prompt = await file.read()
    return prompt


@ai_router.message(Command('random'))
@ai_router.message(F.text == 'Рандомный факт 🧠')
@ai_router.message(F.text == 'Хочу ещё факт 🧠')
async def ai_random_fact(message: Message):
    # Имитация "Бот печатает..."
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING
    )
    prompt = await read_prompt('random.txt')
    completion = await ai_client.chat.completions.create(
        messages=[
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': 'Напиши рандомный факт'}
        ],
        model='gpt-4o'
    )
    photo_file = FSInputFile(path=os.path.join('images', 'random.jpg'))
    caption = completion.choices[0].message.content
    await message.answer_photo(
        photo=photo_file,
        caption=caption,
        reply_markup=kb_random_facts()
    )


@ai_router.message(F.text == 'Задать вопрос ChatGPT 🖥️')
@ai_router.message(Command('gpt'))
async def ai_gpt_command(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join('images', 'gpt.jpg'))
    await message.answer_photo(
        photo=photo_file,
        caption='Напишите ваш запрос к ChatGPT',
        reply_markup=kb_back()
    )
    await state.set_state(FSMStates.wait_for_request)


@ai_router.message(FSMStates.wait_for_request)
async def ai_gpt_request(message: Message, state: FSMContext):
    if message.text == 'Назад 🔙':
        await com_start(message)
    else:
        # Имитация "Бот печатает..."
        await message.bot.send_chat_action(
            chat_id=message.from_user.id,
            action=ChatAction.TYPING
        )
        request = message.text
        prompt = await read_prompt('gpt.txt')
        completion = await ai_client.chat.completions.create(
            messages=[
                {'role': 'system', 'content': prompt},
                {'role': 'user', 'content': request}
            ],
            model='gpt-4o'
        )
        photo_file = FSInputFile(path=os.path.join('images', 'gpt.jpg'))
        caption = completion.choices[0].message.content
        await message.answer_photo(
            photo=photo_file,
            caption=caption,
            reply_markup=kb_start()
        )
    await state.clear()

# @ai_router.message(Command('gpt'))
# async def ai_gpt_request(message: Message):
#     # Имитация "Бот печатает..."
#     await message.bot.send_chat_action(
#         chat_id=message.from_user.id,
#         action=ChatAction.TYPING
#     )
#     _, request = message.text.split(' ', 1)
#     prompt = await read_prompt('gpt.txt')
#     completion = await ai_client.chat.completions.create(
#         messages=[
#             {'role': 'system', 'content': prompt},
#             {'role': 'user', 'content': request}
#         ],
#         model='gpt-3.5-turbo'
#     )
#     photo_file = FSInputFile(path=os.path.join('images', 'gpt.jpg'))
#     caption = completion.choices[0].message.content
#     await message.answer_photo(
#         photo=photo_file,
#         caption=caption,
#         reply_markup=kb_start()
#     )
