from aiogram import Router

from .ai_handlers import ai_router
from .callback_handlers import callback_router
from .command_handlers import command_router
from .keyboards_handlers import keyboard_router

all_handlers_router = Router()
all_handlers_router.include_routers(ai_router, command_router, callback_router, keyboard_router)

__all__ = ['all_handlers_router']
