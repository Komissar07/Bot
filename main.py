import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import all_handlers_router

load_dotenv()


def on_start():
    print('Bot is started...')


def on_shutdown():
    print('Bot is down now...')


async def start_bot():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    dp.include_router(all_handlers_router)
    await bot.delete_webhook(drop_pending_updates=True)  # Пропуск старых апдейтов
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
