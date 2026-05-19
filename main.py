from os import getenv
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.routes import router, notifier
from aiogram.types import BotCommand

load_dotenv()
TOKEN = getenv("BOT_TOKEN")


dp = Dispatcher()
dp.include_router(router)


async def main():
    bot = Bot(token=TOKEN)

    await bot.set_my_commands([
        BotCommand(command='start', description='start the SternBot'),
        BotCommand(command='subscribe', description='subscribe for a regular message' ),
        BotCommand(command='unsubscribe', description='cancel subscription('),
        BotCommand(command='subscribers', description='show the list of subscribers')
    ])

    asyncio.create_task(notifier(bot))
    print("Let's f***")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

