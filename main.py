import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from handlers import start_router, super_admin_router, user_router, simple_admin_router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env файле")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(super_admin_router)
dp.include_router(user_router)
dp.include_router(simple_admin_router)


async def main():
    print("Бот запущен...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
