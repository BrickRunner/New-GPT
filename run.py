import asyncio
import ollama
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from concurrent.futures import ThreadPoolExecutor


# Загрузка переменных окружения
executor = ThreadPoolExecutor()
load_dotenv()
bot = Bot(token=os.getenv('TG_TOKEN'))
dp = Dispatcher()


# Генерация ответа через Ollama с ускорением
def generate_text(prompt: str) -> str:
    response = ollama.chat(
        model="mistral:7b", 
        messages=[
            {"role": "system", "content": "Отвечай кратко и быстро."},
            {"role": "user", "content": prompt}
        ]  
    )
    return response['message']['content']


# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я Dmitry_GPT. Напиши что-нибудь, и я отвечу!")


# Ответ на любое сообщение пользователя через AI
@dp.message()
async def chat_with_ai(message: Message):
    user_text = message.text
    await message.answer("⏳ Думаю...")

    loop = asyncio.get_running_loop()
    ai_response = await loop.run_in_executor(executor, generate_text, user_text)
    await message.answer(ai_response)


# Запуск бота
async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


