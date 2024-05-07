import requests
import time



API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '7109851242:AAFdEjLPgQDUBmBwG_UuV2ayuI7G-TiYGPo'
TEXT = 'Hellow world!'
MAX_COUNTER = 100

offset = -2
counter = 0
chat_id: int


while counter < MAX_COUNTER:

    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            #username = ['message']['chat']['first_name']

            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')

    time.sleep(1)
    counter += 1

# if response.status_code == 200:  # Если код ответа на запрос - 200, то смотрим, что пришло в ответе
#     print(response.text)
# else:
#     print(response.status_code)  # При другом коде ответа выводим этот код