import smtplib
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from email.mime.text import MIMEText

from mailing.models import MailingSettings
from messaging.models import MailingMessage


def send_email(to_email, subject, body):
    # Получение настроек SMTP из файла settings.py
    smtp_host = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_username = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD

    # Создание объекта MIMEMultipart для создания сообщения
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = subject

    # Создание объекта MIMEText для добавления текстового содержимого
    body_content = MIMEText(body, "plain")
    message.attach(body_content)

    # Подключение к SMTP-серверу и отправка сообщения
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)



def send_mailing_message(mailing_id):
    # Получите рассылку по идентификатору
    mailing = MailingSettings.objects.get(id=mailing_id)

    # Получите выбранное сообщение
    message = MailingMessage.objects.get(mailing=mailing)

    # Получите список клиентов, которым нужно отправить рассылку
    clients = mailing.clients.all()

    # Отправьте сообщение каждому клиенту
    for client in clients:
        send_email(client.email, message.subject, message.body)