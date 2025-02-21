import os
from collections import namedtuple

from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import CelebrityData


def ikb_celebrity():
    Celebrity = namedtuple('celebrity', ['name', 'file_name'])
    keyboard = InlineKeyboardBuilder()
    file_list = [file for file in os.listdir('prompts') if file.startswith('talk_')]
    celebrity_list = []
    for file in file_list:
        with open(os.path.join('prompts', file), 'r', encoding='UTF-8') as txt_file:
            name = txt_file.read().split(',', 1)[0][5:].title()
            celebrity_list.append(Celebrity(name, file.rsplit('.', 1)[0]))
    for celebrity in celebrity_list:
        keyboard.button(
            text=celebrity.name,
            callback_data=CelebrityData(
                button='cb',
                name=celebrity.name,
                file_name=celebrity.file_name
            )
        )
    keyboard.adjust(*[1] * len(file_list))
    return keyboard.as_markup()
