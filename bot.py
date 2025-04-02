import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# токен(было лень вставить в .env)
TOKEN = "8003314294:AAGGfcTc7E8FPxUyxy7WyXFrnNn-VkGE3bs"

# настроил логгирование
logging.basicConfig(level=logging.INFO)

# создаем бота и dispathcer
bot = Bot(token=TOKEN)
dp = Dispatcher()

# список дистанций
distance_options = ["5 км", "10 км", "21 км", "42 км"]

# клавиатура с вариантами дистанций
marathon_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="5 км")],
        [KeyboardButton(text="10 км")],
        [KeyboardButton(text="21 км")],
        [KeyboardButton(text="42 км")]
    ],
    resize_keyboard=True
)

user_data = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    # обработка команды |start(запрашивает фио)
    await message.answer("Привет! Введите ваше ФИО для регистрации на марафон.")

# обработка ввода ФИО
# срабатывает, если текст содержит пробел (фио состоит из нескольких слов)
@dp.message(lambda message: message.text
                           and message.text.count(" ") >= 1
                           and message.text not in distance_options
                           and message.from_user.id not in user_data)
async def get_full_name(message: types.Message):
    user_data[message.from_user.id] = {"full_name": message.text}
    await message.answer("Выберите дистанцию марафона:", reply_markup=marathon_keyboard)

# обработка выбора дистанции
# срабатывает только на прописаные варианты
@dp.message(lambda message: message.text in ["5 км", "10 км", "21 км", "42 км"])
async def get_marathon_type(message: types.Message):
    user_data[message.from_user.id]["marathon_type"] = message.text
    full_name = user_data[message.from_user.id]["full_name"]
    await message.answer(
        f"Вы записаны на марафон!\nФИО: {full_name}\nДистанция: {message.text}"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
