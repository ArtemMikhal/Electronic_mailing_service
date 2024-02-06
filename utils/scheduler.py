from apscheduler.schedulers.background import BackgroundScheduler
from mailing.models import MailingSettings
from datetime import datetime, timedelta

from utils.send_mailing import send_mailing_message


def schedule_mailing_messages():
    scheduler = BackgroundScheduler()

    # Получите все рассылки
    mailings = MailingSettings.objects.all()

    # Создайте периодическую задачу для каждой рассылки
    for mailing in mailings:
        # Определите расписание в зависимости от типа периодичности
        if mailing.frequency == 'daily':
            start_date = datetime.now().replace(hour=mailing.send_time.hour, minute=mailing.send_time.minute, second=0,
                                                microsecond=0)
            if start_date < datetime.now():
                start_date += timedelta(days=1)
            scheduler.add_job(send_mailing_message, 'interval', days=1, start_date=start_date, args=[mailing.id])
        elif mailing.frequency == 'weekly':
            start_date = datetime.now().replace(hour=mailing.send_time.hour, minute=mailing.send_time.minute, second=0,
                                                microsecond=0)
            if start_date < datetime.now():
                start_date += timedelta(weeks=1)
            scheduler.add_job(send_mailing_message, 'interval', weeks=1, start_date=start_date, args=[mailing.id])
        elif mailing.frequency == 'monthly':
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            start_date = today.replace(day=mailing.send_time.day, hour=mailing.send_time.hour,
                                       minute=mailing.send_time.minute)
            if start_date < today:
                next_month = today.replace(day=28) + timedelta(days=4)
                start_date = next_month.replace(day=mailing.send_time.day, hour=mailing.send_time.hour,
                                                minute=mailing.send_time.minute)
            scheduler.add_job(send_mailing_message, 'interval', months=1, start_date=start_date, args=[mailing.id])

    scheduler.start()