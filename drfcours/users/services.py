import telegram
from django.utils import timezone
from habbits.models import Habits


bot_token = TG_BOT_TOKEN

def send_telegram_reminder(bot_token, chat_id):
    bot = telegram.Bot(token=bot_token)
    habits_to_remind = Habits.objects.filter(
        last_reminder__lt=timezone.now() - timezone.timedelta(days=1),
        time__hour=timezone.now().hour
    )

    for habit in habits_to_remind:
        try:
            message = f"⏰ Напоминание: {habit.action} в {habit.time.strftime('%H:%M')}"
            bot.send_message(chat_id=chat_id, text=message)

            # Обновляем время последнего напоминания
            habit.last_reminder = timezone.now()
            habit.save()

        except Exception as e:
            print(f"Ошибка при отправке напоминания: {e}")