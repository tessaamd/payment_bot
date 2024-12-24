import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from .services.subscriptions import SubscriptionManager
from .scheduler import setup_scheduler
from .handlers import start_router, payments_router, admin_router
from dotenv import load_dotenv
import os

import sys
import os

# Добавление корневой директории в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .services.subscriptions import SubscriptionManager
from .scheduler import setup_scheduler
from .handlers import start_router, payments_router, admin_router


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")

async def main():
    bot = Bot(token=TOKEN, session=AiohttpSession())
    dp = Dispatcher()

    # Инициализация менеджера подписок
    subscription_manager = SubscriptionManager(
        channel_id=CHANNEL_ID,
        bot=bot
    )

    # Настройка планировщика задач
    setup_scheduler(subscription_manager)

    # Подключение роутеров
    dp.include_routers(
        start_router,
        payments_router,
        admin_router
    )

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
