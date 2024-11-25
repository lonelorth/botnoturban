from gc import callbacks
import os
from aiogram import Bot, Dispatcher,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

api = '7507203863:AAH_Zsisk7Rml3GzwMV1406TRCyLXPv09hk'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())



# ------ Марк ап клавиатура (с кнопками)----------------
kb = ReplyKeyboardMarkup(resize_keyboard=True) # инициализация клавиатуры
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
button3 = KeyboardButton(text='Купить')
kb.row(button)
kb.row(button2)
kb.add(button3)

#-------- Ин лайн клавиатуры (с кнопками)----------------
kb2 = InlineKeyboardMarkup(resize_keyboard=True) # рассчёт калорий человека
in_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

kb2.add(in_button1)
kb2.add(in_button2)

kb3 = InlineKeyboardMarkup(resize_keyboard=True) # покупка продукта
in_button3 = InlineKeyboardButton(text='Продукт1', callback_data='product_buying')
in_button4 = InlineKeyboardButton(text='Продукт2', callback_data='product_buying')
in_button5 = InlineKeyboardButton(text='Продукт3', callback_data='product_buying')
in_button6 = InlineKeyboardButton(text='Продукт4', callback_data='product_buying')
in_button7 = InlineKeyboardButton(text='Продукт5', callback_data='product_buying')
in_button8 = InlineKeyboardButton(text='Продукт6', callback_data='product_buying')

kb3.add(in_button3)
kb3.row(in_button4)
kb3.row(in_button5)
kb3.row(in_button6)
kb3.row(in_button7)
kb3.row(in_button8)

list_img = []
images = './img'
list_img += [each for each in os.listdir(images) if each.endswith('.jpg')]
list_cat = []

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('На текущий момент я пока только могу рассчитать необходимое количество килокалорий (ккал) '
                         'в сутки для каждого конкретного человека. \n По формулуe Миффлина-Сан Жеора, разработанной '
                         'группой американских врачей-диетологов под руководством докторов Миффлина и Сан Жеора. \n'
                         'А ещё пробую создать меню покупок продуктов для здоровья')

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              '\nдля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Данные необходимо вводить целыми числами')
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    mans = (10*int(data['weight'])+6.25*int(data['growth'])-5*int(data['age'])+5)
    wumans = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    await message.answer(f'При таких параметрах норма калорий: \nдля мужчин {mans} ккал в сутки \nдля женщин {wumans} ккал в сутки')
    await UserState.weight.set()
    await state.finish()

@dp.message_handler(text='Купить')
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
            text = f'№{index_img} каталога.\n Наименование: {name_img}.\n Стоймость: {price_img} руб.'
            await message.answer_photo(img, text)
    await message.answer(text='Выберите продукт для покупки: ', reply_markup=kb3)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(text='Вы успешно приобрели продукт!')
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
