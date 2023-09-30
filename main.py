import asyncio
import logging
import sqlite3
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from config import TOKEN

command_list = ['/start', '/help', '/base']
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def command_start_handler(message: Message) -> None:
    await message.answer(f'Hello, {message.from_user.first_name}! Nice to see you!')

@dp.message_handler(commands=['help'])
async def command_help_handler(message: Message) -> None:
    await message.answer(f'available commands {", ".join(command_list)}')

@dp.message_handler(commands=['base'])
async def command_base_handler(message: Message) -> None:
    conn = sqlite3.connect('my_sql.sql')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id int auto_increment primary key,
        name vaechar(50), pass varchar(50)
        )''')
    conn.commit()
    cur.close()
    conn.close()

    await bot.send_message(message.from_user.id, f'Пользователь {message.from_user.first_name} внесен в базу данных')

@dp.message_handler()
async def echo_message(message: Message) -> None:
    await bot.send_message(chat_id=message.from_user.id, text=f'{message.from_user.first_name}, {message.text*2}')

async def main() ->None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())