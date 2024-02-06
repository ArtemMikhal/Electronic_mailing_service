from mailing.models import MailingSettings

def all_messages_created():
    mailings = MailingSettings.objects.all()  # Получаем все рассылки
    for mailing in mailings:
        if not mailing.mailingmessage_set.exists():  # Если для рассылки нет письма
            return False
    return True
