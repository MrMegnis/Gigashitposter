from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from tg.create_bot import bot, dispatcher
from tg.commands import register_handlers


async def on_startup(_):
    print("Бот онлайн!")


def start_bot():
    register_handlers(dispatcher)
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)


if __name__ == "__main__":
    start_bot()
