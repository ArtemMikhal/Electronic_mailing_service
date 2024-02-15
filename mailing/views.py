from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.shortcuts import redirect
from customers.models import Client
from mailing.forms import MailingSettingsForm
from mailing.models import MailingSettings
from messaging.forms import MailingActivateForm
from messaging.models import MailingMessage
from utils.scheduler import schedule_mailing_messages
from django.http import HttpResponseForbidden


class MailingListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    template_name = 'mailing/list.html'
    context_object_name = 'mailings'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        queryset = super().get_queryset()

        # Проверяем, имеет ли пользователь разрешение на просмотр всех рассылок
        if self.request.user.has_perm('mailing.view_mailingsettings'):
            return queryset

        # Фильтруем рассылки по текущему пользователю
        return queryset.filter(user=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    template_name = 'mailing/mailingsettings_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(user=self.request.user).order_by('last_name')
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        mailing_settings = form.save(commit=False)
        mailing_settings.save()  # Сначала сохраняем без связанных клиентов, чтобы присвоить "id"

        selected_clients = form.cleaned_data['clients']

        for client in selected_clients:
            mailing_settings.clients.add(client)

        form.save_m2m()  # Сохраняем связи многие-ко-многим

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(user=self.request.user).order_by('last_name')
        return form

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Проверяем, является ли текущий пользователь создателем рассылки
        if obj.user != self.request.user:
            # Если пользователь не является создателем, генерируем ошибку 403 Forbidden
            raise HttpResponseForbidden("У вас нет прав для редактирования этой рассылки.")
        return obj

    def form_valid(self, form):
        form.instance.user = self.get_object().user
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = MailingSettings
    login_url = reverse_lazy('users:login')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Проверяем, является ли текущий пользователь создателем рассылки
        if obj.user != self.request.user:
            # Если пользователь не является создателем, генерируем ошибку 403 Forbidden
            raise HttpResponseForbidden("У вас нет прав для редактирования этой рассылки.")
        return obj


class MailingActivateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailingSettings
    form_class = MailingActivateForm
    template_name = 'mailing/mailing_activate.html'
    login_url = reverse_lazy('users:login')

    def test_func(self):
        return self.request.user.has_perm('mailing.disable_mailings')

    def form_valid(self, form):
        mailing = form.save(commit=False)
        is_active = form.cleaned_data['is_active']

        if is_active:
            mailing.is_active = True
            print("Рассылка включена")
            # Вызываем функцию schedule_mailing_messages() для запуска рассылки
            schedule_mailing_messages()
        else:
            mailing.is_active = False
            print("Рассылка отключена")
            # Отключаем все задачи рассылки
            scheduler = BackgroundScheduler()
            scheduler.remove_all_jobs()

        mailing.save()

        if mailing.is_active:
            return redirect(reverse('mailing:mailing_detail', kwargs={'pk': mailing.id}))
        else:
            return redirect('mailing:mailing_list')