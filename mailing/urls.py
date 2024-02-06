from django.urls import path

from mailing.views import MailingListView, MailingCreateView, MailingUpdateView, MailingDetailView, MailingDeleteView, MailingActivateView
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='create_mailing'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='update_mailing'),
    path('client/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('activate/<int:pk>/', MailingActivateView.as_view(), name='activate_mailing'),

]