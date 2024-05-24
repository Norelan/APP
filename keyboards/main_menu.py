from aiogram import Bot
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Запустить бота'),
        BotCommand(command='/add',
                   description='Добавить новое желание'),
        BotCommand(command='/watch',
                   description='Посмотреть вишлист'),
        BotCommand(command='/delete',
                   description='Удалить желание'),
        BotCommand(command='/upd_name',
                   description='Изменить желание'),

                   
        # BotCommand(command='/help',
        #            description='Справка по работе бота'),
        # BotCommand(command='/support',
        #            description='Поддержка'),
        # BotCommand(command='/contacts',
        #            description='Другие способы связи'),
        # BotCommand(command='/payments',
        #            description='Платежи')
    ]

    await bot.set_my_commands(main_menu_commands)

