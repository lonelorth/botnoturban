from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = InlineKeyboardMarkup()
button1 = InlineKeyboardButton( text="Информация", callback_data="info")
button2 = InlineKeyboardButton( text="Рассчитать", callback_data="calc")
start_menu.add(button1)
start_menu.add(button2)

kb = InlineKeyboardMarkup()
button3 = InlineKeyboardButton( text="Рассчитать норму калорий", callback_data="calc_normal")
button4 = InlineKeyboardButton( text="Формулы расчета", callback_data="formula")
kb.add(button3)
kb.add(button4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=["start"])
async def start_massage(massage):
    await massage.answer("Привет! Я бот помогающий твоему здоровью.",
                         reply_markup = start_menu)

@dp.callback_query_handler(text = "info")
async def infor(call):
    await call.message.answer("Этот бот поможет вам подсчитать кол-во калорий для вас или показать формулу расчета!")
    await call.answer()

@dp.callback_query_handler(text = "calc")
async def calcu(call):
    await call.message.answer("Выберите опцию:", reply_markup = kb)
    await call.answer()

@dp.callback_query_handler(text = "calc_normal")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

@dp.callback_query_handler(text = "formula")
async def print_form(call):
    await call.message.answer(f"Мужчины: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\nЖенщины: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.")
    await call.answer()

@dp.message_handler(text='Рассчитать норму калорий')
async def set_age(message):
    await message.answer('Введите свой возраст:')
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
    result = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'Ваша норма калорий: {result} ккал в сутки (для мужчин)')
    await UserState.weight.set()
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)