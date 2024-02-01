from django.urls import path

from customers.apps import CustomersConfig
from customers.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDetailView, ClientDeleteView

app_name = CustomersConfig.name

urlpatterns = [
    path('', ClientListView.as_view(), name='list'),
    path('create/', ClientCreateView.as_view(), name='create_client'),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_сlient'),

]