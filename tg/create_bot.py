from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
from dotenv import load_dotenv

load_dotenv('.env')
bot = Bot(token=os.environ.get('BOTTOKEN'))
dispatcher = Dispatcher(bot)
