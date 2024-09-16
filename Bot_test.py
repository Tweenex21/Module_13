from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio


api = "7486861435:AAG63Ug7NaRfvx0ylx8cKmOcIfbWsQG-pqk"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands= ["Start"])
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.' )

@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)