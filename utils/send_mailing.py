import smtplib
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from email.mime.text import MIMEText

from customers.models import Client
from mailing.models import MailingSettings
from mailing_logs.models import MailingLog
from messaging.models import MailingMessage
import logging

def send_email(to_emails, subject, body, mailing_id):
    smtp_host = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_username = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD

    for to_email in to_emails:
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = to_email
        message['Subject'] = subject

        body_content = MIMEText(body, "plain")
        message.attach(body_content)

        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(message)

            mailing_settings = MailingSettings.objects.get(id=mailing_id)
            client = Client.objects.get(client_email=to_email)
            MailingLog.objects.create(mailing=mailing_settings, status='success',
                                      server_response='Письмо успешно отправлено', client=client)
            logging.info(f"Письмо успешно отправлено на адрес {to_email}")
            print(f"Письмо успешно отправлено на адрес {to_email}")
        except Exception as e:
            handle_error(mailing_id, to_email, str(e))


def handle_error(mailing_id, to_email, error_message):
    mailing_settings = MailingSettings.objects.get(id=mailing_id)
    client = Client.objects.get(client_email=to_email)
    MailingLog.objects.create(mailing=mailing_settings, status='failure', server_response=error_message,
                              client=client)
    logging.error(f"Ошибка: {error_message}, Адрес электронной почты: {to_email}")
    print(f"Ошибка: {error_message}, Адрес электронной почты: {to_email}")
def send_mailing_message(mailing_id):
    mailing_settings = MailingSettings.objects.get(id=mailing_id)
    message = MailingMessage.objects.get(mailing=mailing_settings)
    clients = mailing_settings.clients.all()

    client_emails = [client.client_email for client in clients]
    send_email(client_emails, message.subject, message.body, mailing_id)