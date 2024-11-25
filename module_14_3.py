import os
from aiogram import Bot, executor
from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keywboards import *
from config import *


api = '*'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


genders = 5
activ = 1
set_weights = 1
set_growths_ = 1
set_ages = 1
calories = 0
list_img = []
images = './img'
list_img += [each for each in os.listdir(images) if each.endswith('.jpg')]
list_cat = []


class UserState(StatesGroup):
    global set_weights
    global set_growths_
    global set_ages
    age = State()
    growth = State()
    weight = State()
    calories = State()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    text = ('Для мужчин:\n(10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5) x активность'
            '\n\nДля женщин:\n(10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) -161) x активность')
    await call.message.answer(text)
    await call.answer()


@dp.message_handler(text='info')
async def inform(message):
    text = ("Этот бот поможет вам подсчитать кол-во калорий для вас или показать формулу расчета!")
    await message.answer(text)


@dp.callback_query_handler(text=['5'])
@dp.callback_query_handler(text=['-161'])
async def start_message(call):
    global genders
    genders = float(call.data)
    await call.answer()
    await call.message.answer('Выберите опцию:', reply_markup=key_setting)
    await call.answer()
    return genders


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст (число, от 0 до 100):')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    global set_ages
    await state.update_data(age=message.text)
    counting = await state.get_data()
    rep_age = str(counting['age']).replace(",", ".")
    try:
        set_ages = float(rep_age)
        if set_ages <= 100:
            await state.update_data(age=set_ages)
            await message.answer('Введите свой рост (число):')
            await UserState.growth.set()
        else:
            await message.answer(err_age)
            return set_age()
    except ValueError:
        await message.answer(err_age)
        return set_age()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    counting = await state.get_data()
    rep_growth = str(counting['growth']).replace(",", ".")
    try:
        set_growths = float(rep_growth)
        await state.update_data(growth=set_growths)
        await message.answer('Введите свой вес (число):')
        await UserState.weight.set()
    except ValueError:
        await message.answer(err_number)
        return set_growth()


@dp.callback_query_handler(text='1.2')
@dp.callback_query_handler(text='1.375')
@dp.callback_query_handler(text='1.55')
@dp.callback_query_handler(text='1.7')
@dp.callback_query_handler(text='1.9')
async def get_active(call):
    global calories
    global set_ages
    global set_growths_
    global set_weights
    global activ
    await call.answer()
    activ = float(call.data)
    calories = float((10 * set_weights + 6.25 * set_growths_ - 5 * set_ages + genders) * activ)
    await call.message.answer(f'Ваша норма калорий: {round(calories, 2)}')
    return calories


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    global calories
    global set_ages
    global set_growths_
    global set_weights
    global activ
    await state.update_data(weight=message.text)
    counting = await state.get_data()
    rep_weight = str(counting['weight']).replace(",", ".")
    try:
        set_weights = float(rep_weight)
        await state.update_data(weight=set_weights)
        counting = await state.get_data()
        set_growths_ = counting['growth']
        set_ages = counting['age']
        await message.answer('Выберите свою активность:', reply_markup=key_activ)
        await state.finish()
    except ValueError:
        await message.answer(err_number)
        return set_weight()


@dp.callback_query_handler(text='product_buying')
async def get_buying_list(call):
    global list_cat
    name_set = str(call.message.caption)
    name_set1 = name_set[:name_set.find('-')] if '-' in name_set else name_set
    for i in list_cat:
        for index, (key, value) in enumerate(i.items()):
            x = str(key)
            if x == name_set1:
                print(f'\033[31mПоздравляю с покупкой!\n{value[1]} по цене: {value[2]} руб.\033[0m')
                await call.message.answer(f'Поздравляю с покупкой!\n{value[1]} по цене: {value[2]} руб.')
    await call.answer()


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    global list_cat
    list_cat = []
    for i in range(len(list_img)):
        with open(f'{images}/{list_img[i]}', 'rb') as img:
            full_img = list_img[i].replace(".jpg", "")
            j = full_img.split('_')
            index_img = j[0]
            name_img = j[1]
            price_img = j[2]
            price_img = str(price_img).replace(".jpg", ".")
            catalog = {j[0]: (j[0], j[1], j[2])}
            list_cat.append(catalog)
            text = f'№{index_img} каталога.\n Наименование: {name_img}'
            key_shop = InlineKeyboardMarkup(resize_keyboard=True)
            bt = InlineKeyboardButton(text=f'Купить за: {price_img} руб.', callback_data='product_buying')
            key_shop.add(bt)
            await message.answer_photo(img, text, reply_markup=key_shop)


@dp.message_handler(text=['Калории'])
async def menu_calories(message):
    text = 'Привет, я бот помогающий твоему здоровью!\nВыберите ваш пол:'
    await message.answer(text, reply_markup=key_gender)


@dp.message_handler(text='start')
async def start(message):
    text = f'Здравствуйте, {message.from_user.username}!\nВыберите нужный пункт:'
    await message.answer(text, reply_markup=key_menu)


@dp.message_handler()
async def all_message(message):
    await message.answer('Нажмите кнопку "start", или "info" чтобы начать общение.', reply_markup=key_start)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
