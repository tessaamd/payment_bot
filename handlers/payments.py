from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from services.subscriptions import SubscriptionManager

router = Router()

@router.message(commands=["buy"])
async def buy_handler(message: Message):
    buttons = [
        [InlineKeyboardButton(text="Неделя - $1.99", callback_data="plan_week")],
        [InlineKeyboardButton(text="Месяц - $12", callback_data="plan_month")],
        [InlineKeyboardButton(text="Год - $100", callback_data="plan_year")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выберите тариф:", reply_markup=keyboard)

@router.callback_query(F.data.in_(["plan_week", "plan_month", "plan_year"]))
async def subscription_handler(callback: CallbackQuery, subscription_manager: SubscriptionManager):
    durations = {"plan_week": 7, "plan_month": 30, "plan_year": 365}
    duration = durations[callback.data]

    subscription_manager.add_subscription(callback.from_user.id, duration)

    invite_link = await subscription_manager.create_personal_invite(
        user_id=callback.from_user.id,
        expiry_seconds=3600
    )

    if invite_link:
        await callback.message.answer(
            f"Вы успешно оплатили подписку: {invite_link}\n"
        )
    else:
        await callback.message.answer("Ошибка создания ссылки")
