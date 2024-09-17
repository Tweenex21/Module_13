from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
import asyncio



api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands= ["Start"])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Сalories")
async def set_age(message: Message):
    await message.answer('Введите свой возраст.')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)  # Исправление опечатки
    await message.answer("Введите свой вес")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data["age"])
    growth = int(data["growth"])
    weight = int(data["weight"])

    # Для примера я буду считать, что пол пользователя "male", так как gender неизвестен
    data = 10 * weight + 6.25 * growth - 5 * age + 5  # Расчет для мужчины

    await message.answer(f"Ваша норма калорий: {data}")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)