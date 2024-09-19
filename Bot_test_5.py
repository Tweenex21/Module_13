from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from  aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = "7486861435:AAG63Ug7NaRfvx0ylx8cKmOcIfbWsQG-pqk"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button3 = KeyboardButton(text='Расcчитать')
button4 = KeyboardButton(text='Информация')
kb.insert(button3)
kb.insert(button4)

inline_menu = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_menu.insert(button1)
inline_menu.insert(button2)



@dp.message_handler(commands= ['Start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Информация')
async def Inform(message):
    await message.answer('В этой информации куда зачислять деньги --> +7999-234-21-88!)')

@dp.message_handler(text='Расcчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_menu)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула рассчета сжигания ЖИРА!\nдля мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х '
                              'возраст (г) + 5')
    await call.answer()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data["age"])
    growth = int(data["growth"])
    weight = int(data["weight"])
    data = 10 * weight + 6.25 * growth - 5 * age + 5  # Расчет для мужчины
    await message.answer(f"Ваша норма калорий: {data}")
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)