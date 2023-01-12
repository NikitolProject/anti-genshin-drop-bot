import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv

load_dotenv(".env")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ["TOKEN"])

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
