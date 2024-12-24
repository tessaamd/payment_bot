from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from services.subscriptions import SubscriptionManager

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, subscription_manager: SubscriptionManager):
    if subscription_manager.check_subscription(message.from_user.id):
        await message.answer("У вас активная подписка! Добро пожаловать.")
    else:
        await message.answer(
            "Подписка отсутствует или истекла. Выберите тариф и получите новую ссылку на вход."
        )
