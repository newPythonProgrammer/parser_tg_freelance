from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())




