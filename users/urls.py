from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, VerifyAccountView, VerificationMessageView, UsersListView, \
    UserBlockedView, UsersDeleteView, UsersDetailView, CustomLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('verify/<str:uidb64>/<str:token>/', VerifyAccountView.as_view(), name='verify_account'),
    path('verification-message/', VerificationMessageView.as_view(), name='verification_message'),
    path('user_blocked/<int:pk>/', UserBlockedView.as_view(), name='user_blocked'),
    path('users_list/', UsersListView.as_view(), name='users_list'),
    path('delete/<int:pk>/', UsersDeleteView.as_view(), name='delete_user'),
    path('client/<int:pk>/', UsersDetailView.as_view(), name='users_detail'),

]