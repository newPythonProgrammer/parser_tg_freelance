from aiogram.utils import executor
from handlers.client import register_client
from handlers.admin import register_admin
import config
from bot import bot, dp



async def main(_):#Функция выполняется при запуске
    for admin in config.ADMINS:
        try:
            await bot.send_message(admin, 'Бот запущен!')
        except:
            pass


register_client(dp)
register_admin(dp)
executor.start_polling(dp, on_startup=main)