from aiogram import Router, F 
from aiogram.filters import Command  
from aiogram.types import (
    Message,
    FSInputFile
)
from forms.user import Form
from aiogram.fsm.context import FSMContext
import aiosqlite
from aiogram import Bot
import asyncio 


router = Router()

import aiohttp

DB_NAME = "users_info.sql"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         full_name TEXT,
                         age INTEGER
                         )
                         """)
        await db.commit()


async def add_user(full_name, age):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO users(full_name, age) VALUES(?, ?)", (full_name, age))
        await db.commit()


async def get_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT full_name, age FROM users")
        result = await cursor.fetchall()
        return result
    
subscribers = set()
subscribers_username = set()


async def notifier(bot: Bot):
    while True:
        if subscribers:
            time = 0
            for user_id in list(subscribers):
                try:
                    time += 5
                    await bot.send_message(user_id, f"{time} seconds passed")
                except Exception:
                    pass
        await asyncio.sleep(5)

@router.message(Command('subscribe'))
async def subscribe(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    subscribers.add(user_id)
    subscribers_username.add(username)

    await message.answer('You are subscribed now!🎉🎉🎉')


@router.message(Command('unsubscribe'))
async def unsubscribe(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    subscribers.discard(user_id)
    subscribers_username.discard(username)

    await message.answer('You unsubscribed :(')


@router.message(Command('subscribers'))
async def subcribers_cmd(message: Message):
    admin_id = 1273261277
    if not message.from_user.id == admin_id:
        await message.answer('Command is unavailable.')
        return
    if not subscribers:
        await message.answer('Subscribers list is empty...')
        return
    text = 'Subscribers:\n'
    for u_id in subscribers:
        text += f"ID: <code>{u_id}</code>"
    
    for username in subscribers_username:
        text += f"-- @{username}\n"
    await message.answer(text, parse_mode='html')
    


@router.message(Command('start'))
async def start(message: Message):
    await init_db()
    await message.answer("Salom! 🐪\nSend a command /reg <i>your age</i>\nI can help with mailing!\n\nCommands:\n/subscribe - turn on notifications\n"
    "/unsubscribe - cancel subscription\n"
    "/subscribers - list of subs", parse_mode='html')


@router.message(Command('reg'))
async def reg(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer('Please, enter the data correctly.')
        return
    await add_user(message.from_user.full_name, int(parts[1]))

    await message.answer("Registration is done!")


@router.message(Command('users'))
async def users(message: Message):
    users = await get_users()

    if not users:
        await message.answer("No users")
        return
    
    text = "Users in base:\n\n"

    for full_name, age in users:
        text += f"- {full_name} - <code>{age}</code>\n"
    
    await message.answer(text, parse_mode='html')
     