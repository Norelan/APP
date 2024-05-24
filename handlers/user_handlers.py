from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import LEXICON
from databse.database import BotDB

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
router = Router()

class Reg_Wish(StatesGroup):
    name = State()
    url = State()

class Upd_Wish(StatesGroup):
    name = State()
    id = State()


class Del_Wish(StatesGroup):
    id = State()

@router.message(CommandStart())
async def process_start_command(message: Message):

    if (not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.answer(LEXICON[message.text])
    
@router.message(Command('add'))
async def add_wish(message: Message, state: FSMContext):
    await state.set_state(Reg_Wish.name)
    await message.answer("Введите назание желания")

@router.message(Reg_Wish.name)
async def wish_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg_Wish.url)
    await message.answer("Введите ссылку ")

@router.message(Reg_Wish.url)
async def wish_url(message: Message, state: FSMContext):

    await state.update_data(url=message.text)
    data = await state.get_data()
    await state.clear()

    wish_text, wis_url = data["name"], data["url"]
    await message.answer(f'Желание добавлено. \n {wish_text} \n {wis_url}  ')
    BotDB.add_wish(message.from_user.id, wish_text, wis_url)

@router.message(Command('watch'))
async def add_wish(message: Message):
    wislist = BotDB.get_wishlist(message.from_user.id)
    answer = f'Вот ваш вишлист  \n\n'
    for w in wislist:
        answer += f'🟢{w[2]} \n id желания {w[0]} \n\n'
    
    print(wislist[0][2])
    await message.answer(answer)

@router.message(Command('delete'))
async def del_wish(message: Message, state: FSMContext):
    await state.set_state(Del_Wish.id)
    await message.answer("Введите назание желания, которое желаете удалить")

@router.message(Del_Wish.id)
async def del_wish_2(message: Message, state: FSMContext):
    #await state.update_data(id=message.text)
    #data = await state.get_data()
    await state.clear()

    owner = BotDB.wish_owner(int(message.text))
    owner_id = BotDB.get_id(message.from_user.id)
    if owner == owner_id:
        BotDB.delete_wish(int(message.text))
        await message.answer("Желание было удалено")
    else: 
        await message.answer("Вы не можете удалить это желание")
    

@router.message(Command('upd_name'))
async def upd_wish_name(message: Message, state: FSMContext):
    await state.set_state(Upd_Wish.id)
    await message.answer("Введите id желания ")

@router.message(Upd_Wish.id)
async def upd_wish_name2(message: Message, state: FSMContext):
    await state.set_state(Upd_Wish.name)
    
    owner = BotDB.wish_owner(int(message.text))
    owner_id = BotDB.get_id(message.from_user.id)
    print(owner)
    print(owner_id)

    if owner == owner_id:
        await state.update_data(id=int(message.text))
        BotDB.update_wish_text(int(message.text), int(message.text) )
        await message.answer("Введите новое название")
    else: 
        await message.answer("Вы не можете изменять это желание")

@router.message(Upd_Wish.name)
async def upd_wish_name3(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    BotDB.update_wish_text(message.text, data["id"] )
    await message.answer("Название было обновлено")






@router.message()
async def else_command(message: Message):
    await message.answer('Такой команды я не знаю. \n Посмотри в меню, там описан весь мой функционал')
    # if message.from_user.id not in users_db:
    #     users_db[message.from_user.id] = deepcopy(user_dict_template)
