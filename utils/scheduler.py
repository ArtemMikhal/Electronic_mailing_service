from apscheduler.schedulers.background import BackgroundScheduler
from mailing.models import MailingSettings
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from utils.send_mailing import send_mailing_message

def schedule_mailing_messages():
    scheduler = BackgroundScheduler()

    # Получите все настройки рассылки
    mailings = MailingSettings.objects.all()

    # Создайте периодическую задачу для каждой рассылки
    for mailing in mailings:
        # Определите расписание на основе типа частоты
        if mailing.frequency == 'daily':
            send_time = datetime.combine(date.today(), datetime.min.time()) + timedelta(hours=mailing.send_time.hour,
                                                                                        minutes=mailing.send_time.minute)
            start_date = send_time
            if start_date < datetime.now():
                start_date += timedelta(days=1)
            scheduler.add_job(send_mailing_message, 'interval', days=1, start_date=start_date, args=[mailing.id])
        elif mailing.frequency == 'weekly':
            send_time = datetime.combine(date.today(), datetime.min.time()) + timedelta(hours=mailing.send_time.hour,
                                                                                        minutes=mailing.send_time.minute)
            start_date = send_time
            if start_date < datetime.now():
                start_date += timedelta(weeks=1)
            scheduler.add_job(send_mailing_message, 'interval', weeks=1, start_date=start_date, args=[mailing.id])
        elif mailing.frequency == 'monthly':
            send_time = datetime.combine(date.today(), datetime.min.time()) + timedelta(hours=mailing.send_time.hour,
                                                                                        minutes=mailing.send_time.minute)
            start_date = send_time
            if start_date < datetime.now():
                next_month = datetime.now().replace(day=1) + relativedelta.relativedelta(months=1)
                start_date = datetime.combine(next_month.date(), send_time.time())
            scheduler.add_job(send_mailing_message, 'date', run_date=start_date, args=[mailing.id])

    scheduler.start()