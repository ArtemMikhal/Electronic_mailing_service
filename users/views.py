from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View, ListView, DetailView, DeleteView
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm, UserBlockedForm
from users.models import User


class CustomLoginView(LoginView):
    def form_valid(self, form):
        if self.request.user.is_authenticated and not self.request.user.is_verified:
            messages.error(self.request, 'Ваш аккаунт не подтвержден. Подтвердите его на электронной почте.')
        return super().form_valid(form)


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    login_url = reverse_lazy('users:login')
    permission_required = 'users.view_user'


class UsersDetailView(LoginRequiredMixin, PermissionRequiredMixin,  DetailView):
    model = User
    permission_required = 'users.view_user'

class UsersDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('main:home')
    success_message = "Ваш аккаунт успешно удален."

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.request.user.pk)

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('main:home')


class UserBlockedView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserBlockedForm
    template_name = 'users/user_blocked.html'
    success_url = reverse_lazy('users:users_list')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Отправка письма с подтверждением
        user = form.save(commit=False)
        current_site = get_current_site(self.request)
        mail_subject = 'Подтвердите ваш аккаунт'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_url = self.request.build_absolute_uri(
            reverse('users:verify_account', kwargs={'uidb64': uid, 'token': token}))
        message = f"Здравствуйте {user.username},\n\nПожалуйста, подтвердите ваш аккаунт, перейдя по следующей ссылке:\n\n{activation_url}\n\nЕсли вы не регистрировались на нашем сайте, проигнорируйте это письмо."

        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        # Сохранение токена в базе данных
        user.activation_token = token
        user.save()

        print("User PK:", user.pk)
        print("Token:", token)
        return response

    def get_success_url(self):
        # Перенаправление на страницу с сообщением о необходимости подтверждения аккаунта
        return reverse_lazy('users:verification_message')


class VerifyAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            login_url = reverse('users:login')  # Получаем URL страницы входа в аккаунт
            message = 'Аккаунт успешно подтвержден. Теперь вы можете <a href="{}">войти</a>.'.format(login_url)
            return HttpResponse(message)
        else:
            return HttpResponse('Недействительная ссылка подтверждения аккаунта.')


class VerificationMessageView(TemplateView):
    template_name = 'users/verification_message.html'


