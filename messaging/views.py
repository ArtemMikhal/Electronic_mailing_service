from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView

from mailing.models import MailingSettings
from messaging.forms import MailingMessageForm
from messaging.models import MailingMessage



class MessagingCreateView(LoginRequiredMixin, CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    template_name = 'messaging/mailingmessage_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['mailing'].queryset = MailingSettings.objects.filter(user=self.request.user)

        # Исключение из списка рассылок тех, для которых уже создано письмо
        existing_mailings = MailingMessage.objects.values_list('mailing', flat=True)
        form.fields['mailing'].queryset = form.fields['mailing'].queryset.exclude(pk__in=existing_mailings)

        return form

class MessagingUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['mailing'].queryset = MailingSettings.objects.filter(user=self.request.user)
        form.fields['mailing'].disabled = True
        return form

    def form_valid(self, form):
        original_mailing = self.get_object().mailing
        new_mailing = form.cleaned_data['mailing']

        # Проверка, существует ли уже письмо для выбранной рассылки
        if new_mailing != original_mailing and MailingMessage.objects.filter(mailing=new_mailing).exists():
            form.add_error('mailing', 'Для этой рассылки письмо уже создано!')
            return self.form_invalid(form)

        return super().form_valid(form)


class MessagingDetailView(LoginRequiredMixin, DetailView):
    model = MailingMessage
    login_url = reverse_lazy('users:login')


class MessagingDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')



