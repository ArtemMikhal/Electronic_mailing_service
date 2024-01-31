from django.urls import path


from main.views import HomeView

from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

]