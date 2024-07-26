import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
from quiz_data import quiz_data

import database_requests as dbr
import command_handlers as ch

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = 'YOUR_TOKEN'

# Объект бота
bot = Bot(token=API_TOKEN)

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )

    builder.adjust(1)
    return builder.as_markup()

# Запуск процесса поллинга новых апдейтов
async def main():

    # Запускаем создание таблицы базы данных
    await dbr.create_table()

    await ch.dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())