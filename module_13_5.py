from  aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio


api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информация')
kb.row(button, button2)


class UserState(StatesGroup):  #собираем данные
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands= ['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)
    # await message.answer('Введи /Calories посчитаю необходимое количество ккал/сутки')


@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer('Введи свой возраст:')
    await UserState.age.set()   #запись возраста


@dp.message_handler()
async def all_message(message):
    await message.answer('Введи команду /start, чтобы начать общение.')


@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    try:
        await state.update_data(age = float(message.text))
    except:
        await message.answer('Введи число, свой возраст')
        return set_age()
    await message.answer('Введи свой рост в см:')
    await UserState.growth.set()


@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    try:
        await state.update_data(growth = float(message.text))
    except:
        await message.answer('Введите число, свой рост')
        return set_growth()
    await message.answer('Введи свой вес:')
    await UserState.weight.set()


@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    try:
        await state.update_data(weight =float(message.text))
    except:
        await message.answer('Введи число, свой вес')
        return send_calories()
    data = await state.get_data()
    calories = (10 * data['weight'] + 6.25 * data['growth'] -
                5 * data['age'] - 161)
    await message.answer(f'Твоя норма калорий {calories}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)

