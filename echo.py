from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ContentType
from aiogram import F
import requests
BOT_TOKEN = '7109851242:AAFdEjLPgQDUBmBwG_UuV2ayuI7G-TiYGPo'

API_FOX_URL = 'https://randomfox.ca/floof/'
API_URL = 'https://api.telegram.org/bot'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



async def process_start_command(message: Message):
    await message.answer('Привет!\n Меня зовут Wish-бот!\n Пока что я не умею составлять вишлисты, но могу отправить вам фото лисички.\n Напиши мне что-нибудь')


async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе картинку лисы'
    )

async def send_photo_echo(message: Message):
    print(message)
    await message.reply_photo(message.photo[0].file_id)



async def send_echo(message: Message):

    fox_response = requests.get(API_FOX_URL)
    if fox_response.status_code == 200:
        fox_link = fox_response.json()['image']
    else:
        await message.answer('Что-то пошло не так')

    await message.reply(text=f'Я могу повторить ваше сообщение')
    await message.send_copy(chat_id=message.chat.id)
    await message.answer('И вот вам Лиса')
    await bot.send_photo(chat_id=message.chat.id, photo=fox_link)

dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(send_photo_echo, F.content_type == ContentType.PHOTO)
dp.message.register(send_echo)

   

if __name__ == '__main__':
    dp.run_polling(bot)