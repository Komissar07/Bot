import os

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from fsm.states import CelebrityDialog
from keyboards import kb_back
from keyboards.callback_data import CelebrityData

callback_router = Router()


@callback_router.callback_query(CelebrityData.filter(F.button == 'cb'))
async def select_celebrity(callback: CallbackQuery, callback_data: CelebrityData, state: FSMContext):
    await state.set_state(CelebrityDialog.wait_for_answer)
    await state.update_data(name=callback_data.name, dialog=[], prompt=callback_data.file_name)
    photo_file = FSInputFile(path=os.path.join('images', callback_data.file_name + '.jpg'))
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo_file,
        caption=f'Вас приветствует {callback_data.name}!\n\nНачните диалог первым...',
        reply_markup=kb_back()
    )
