from django.urls import path
from mailing_logs.apps import MailingLogsConfig
from mailing_logs.views import MailingLogsListView

app_name = MailingLogsConfig.name

urlpatterns = [
    path('', MailingLogsListView.as_view(), name='logs_list'),


]