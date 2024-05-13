
from aiogram import Bot, Dispatcher, F
from config_data.config import Config, load_config
from handlers import user_handlers
from aiogram.types import BotCommand
from aiogram.filters import Command, CommandStart
from keyboards.main_menu import set_main_menu


config: Config = load_config()

bot = Bot(token=config.tg_bot.token)
dp = Dispatcher()


dp.startup.register(set_main_menu)
# Регистрируем роутеры в диспетчере
dp.include_router(user_handlers.router)
print(config.tg_bot.admin_ids)


if __name__ == '__main__':
    dp.run_polling(bot)