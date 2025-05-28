from celery import shared_task
from .services import send_telegram_reminder

@shared_task
def check_and_send_reminders():
    send_telegram_reminder(
        bot_token='',
        chat_id=''
    )