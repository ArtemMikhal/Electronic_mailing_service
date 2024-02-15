from django.urls import path
from messaging.views import MessagingCreateView, MessagingDetailView, MessagingDeleteView, MessagingUpdateView
from messaging.apps import MessagingConfig


app_name = MessagingConfig.name

urlpatterns = [
    path('create/', MessagingCreateView.as_view(), name='create_messaging'),
    path('message/<int:pk>/', MessagingDetailView.as_view(), name='messaging_detail'),
    path('delete/<int:pk>/', MessagingDeleteView.as_view(), name='delete_messaging'),
    path('update/<int:pk>/', MessagingUpdateView.as_view(), name='update_messaging'),
]