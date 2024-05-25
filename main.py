
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import user_handlers
from keyboards.main_menu import set_main_menu
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


config: Config = load_config()

bot = Bot(token=config.tg_bot.token, default = DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

#Подключаю клавиатуру
dp.startup.register(set_main_menu)


# Регистрируем роутеры в диспетчере
dp.include_router(user_handlers.router)
print(config.tg_bot.admin_ids)

if __name__ == '__main__':
    dp.run_polling(bot)