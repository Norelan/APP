import requests
import time



API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '7109851242:AAFdEjLPgQDUBmBwG_UuV2ayuI7G-TiYGPo'
TEXT = 'Hellow world!'


response = requests.get(f'https://api.telegram.org/bot7109851242:AAFdEjLPgQDUBmBwG_UuV2ayuI7G-TiYGPo/getMe')



if response.status_code == 200:  # Если код ответа на запрос - 200, то смотрим, что пришло в ответе
    print(response.text)
else:
    print(response.status_code)  # При другом коде ответа выводим этот код