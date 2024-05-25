from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup, 
                           InlineKeyboardButton, InlineKeyboardMarkup,)

# Создаем объекты кнопок
button_1 = KeyboardButton(text='Мой вишлист 🎁')
button_2 = KeyboardButton(text='Друзья 🥳')

# Создаем объект клавиатуры, добавляя в него кнопки
keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]],
    resize_keyboard=True,
    one_time_keyboard=True)

# Клавиатура для вишлиста
button_add = InlineKeyboardButton(
    text='Добавить новое желание',
    callback_data='/add'
)

keyboard_wishlist = InlineKeyboardMarkup(
    inline_keyboard=[[button_add]])

# Клавиатура конкретного желания
upd_name_button = InlineKeyboardButton(
    text='Редактировать название',
    callback_data='/upd_name'
)

upd_url_button = InlineKeyboardButton(
    text='Редактировать ссылку',
    callback_data='/upd_url'
)
delete_button = InlineKeyboardButton(
    text='Удалить желание',
    callback_data='/delete'
)

keyboard_wish = InlineKeyboardMarkup(
    inline_keyboard=[[upd_name_button],
                     [upd_url_button],
                     [delete_button]])
