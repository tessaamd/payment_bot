from datetime import datetime, timedelta
from aiogram import Bot

SUBSCRIPTIONS = {}

class SubscriptionManager:
    def __init__(self, channel_id: str, bot: Bot):
        self.channel_id = channel_id
        self.bot = bot

    def add_subscription(self, user_id: int, duration: int):
        SUBSCRIPTIONS[user_id] = datetime.now() + timedelta(days=duration)

    def check_subscription(self, user_id: int) -> bool:
        return user_id in SUBSCRIPTIONS and SUBSCRIPTIONS[user_id] > datetime.now()

    async def create_personal_invite(self, user_id: int, expiry_seconds: int = 3600) -> str:
        try:
            invite = await self.bot.create_chat_invite_link(
                chat_id=self.channel_id,
                expire_date=datetime.now() + timedelta(seconds=expiry_seconds),
                member_limit=1
            )
            return invite.invite_link
        except Exception as e:
            print(f"Ошибка создания ссылки: {e}")
            return None

    async def remove_expired_users(self):
        now = datetime.now()
        for user_id, expiry_date in list(SUBSCRIPTIONS.items()):
            if expiry_date < now:
                try:
                    await self.bot.kick_chat_member(chat_id=self.channel_id, user_id=user_id)
                    del SUBSCRIPTIONS[user_id]
                except Exception as e:
                    print(f"Ошибка удаления {user_id}: {e}")

    async def notify_users(self):
        now = datetime.now()
        for user_id, expiry_date in SUBSCRIPTIONS.items():
            days_left = (expiry_date - now).days
            if days_left == 7:
                try:
                    await self.bot.send_message(
                        chat_id=user_id,
                        text="Обнови свою подписку. Она скоро истечет!"
                    )
                except Exception as e:
                    print(f"Ошибка уведомления {user_id}: {e}")
