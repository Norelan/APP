from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import LEXICON
from databse.database import DB

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from keyboards.keyboard import keyboard, keyboard_wishlist, keyboard_wish
from aiogram.types import CallbackQuery
import re
router = Router()
BotDB = DB('wish.db')

class Reg_Wish(StatesGroup):
    name = State()
    url = State()

class Upd_Wish(StatesGroup):
    name = State()
    id = State()
    url = State()

class Del_Wish(StatesGroup):
    id = State()

@router.message(CommandStart())
async def process_start_command(message: Message):

    if (not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.answer(text = LEXICON[message.text], reply_markup=keyboard )
    
# Добавление нового желания
@router.callback_query(F.data.in_(['/add']))
async def add_wish(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Reg_Wish.name)
    await callback.message.answer("Введите назание желания:")
    await callback.answer()

@router.message(Reg_Wish.name)
async def wish_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg_Wish.url)
    await message.answer("Введите ссылку: ")

@router.message(Reg_Wish.url)
async def wish_url(message: Message, state: FSMContext):

    await state.update_data(url=message.text)
    data = await state.get_data()
    await state.clear()

    wish_text, wis_url = data["name"], data["url"]
    await message.answer(f'Желание добавлено ')
    BotDB.add_wish(message.from_user.id, wish_text, wis_url)
    await watch_wishlist(message)

# Отображение
@router.message(F.text == 'Мой вишлист 🎁')
async def watch_wishlist(message: Message, user_id=None):
    if user_id is None:
        user_id = message.from_user.id
    wishlist = BotDB.get_wishlist(user_id)

    if not wishlist:
        await message.answer("Ваш вишлист пуст.", reply_markup=keyboard_wishlist)
    else:
        answer = f'Вот ваш вишлист  \n\n'
        for w in wishlist:
            answer += f'🟢{w[2]} \n id желания /wish{w[0]} \n\n'
            await message.answer(text = answer, reply_markup=keyboard_wishlist)

# Показ желания 
@router.message(lambda message: re.match(r'^/wish(\d+)$', message.text))
async def watch_wish(message: Message, state: FSMContext):
    await state.set_state(Upd_Wish.id)

    match = re.match(r'^/wish(\d+)$', message.text)
    if not match:
        await message.answer("Invalid command format.")
        return
    
    wish_id = int(match.group(1))
    
    owner = BotDB.wish_owner(wish_id)
    owner_id = BotDB.get_id(message.from_user.id)

    if owner == owner_id:
        await state.update_data(id = wish_id)
        wish = BotDB.get_wish(wish_id)[0]
        await message.answer(text = f"{wish[2]}, \n {wish[3]}", reply_markup=keyboard_wish)
    else: 
        await message.answer("Вы не можете просматривать это желание")


# Удаление
@router.callback_query(F.data.in_(['/delete']))
async def del_wish(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    BotDB.delete_wish(data["id"])
    try:
        await callback.message.delete()  # Удаление исходного сообщения с кнопкой
        
    except:
        pass

    await callback.message.answer("Желание было удалено")

    await watch_wishlist(callback.message, callback.from_user.id)
   


# Редактирование
@router.callback_query(F.data.in_(['/upd_name']))
async def upd_get_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Upd_Wish.name)
    await callback.message.answer("Введите новое название:")

@router.message(Upd_Wish.name)
async def upd_wish_name(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    BotDB.update_wish_text(message.text, data["id"] )
    await message.answer("Название было обновлено")

@router.callback_query(F.data.in_(['/upd_url']))
async def upd_get_url(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Upd_Wish.url)
    await callback.message.answer("Введите новую ссылку:")

@router.message(Upd_Wish.url)
async def upd_wish_url(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    BotDB.update_wish_url(message.text, data["id"] )
    await message.answer("Ссылка была обновлена")

# Исключения
@router.message()
async def else_command(message: Message):
    await message.answer('Такой команды я не знаю. \n Посмотри в меню, там описан весь мой функционал')
    # if message.from_user.id not in users_db:
    #     users_db[message.from_user.id] = deepcopy(user_dict_template)
