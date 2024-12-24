from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .services.subscriptions import SubscriptionManager

def setup_scheduler(subscription_manager: SubscriptionManager):
    scheduler = AsyncIOScheduler()

    scheduler.add_job(subscription_manager.remove_expired_users, "interval", hours=24)
    scheduler.add_job(subscription_manager.notify_users, "interval", hours=24)

    scheduler.start()
    return scheduler
