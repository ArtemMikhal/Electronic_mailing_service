from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from customers.models import Client
from mailing.forms import MailingSettingsForm
from mailing.models import MailingSettings
from messaging.forms import MailingActivateForm
from messaging.models import MailingMessage
from utils.scheduler import schedule_mailing_messages


class MailingListView(ListView):
    model = MailingSettings

class MailingCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    template_name = 'mailing/mailingsettings_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TIME_CHOICES'] = MailingSettings.TIME_CHOICES
        context['clients'] = Client.objects.order_by('last_name')
        return context

    def form_valid(self, form):
        mailing_settings = form.save(commit=False)
        mailing_settings.save()  # Сначала сохраняем без связанных клиентов, чтобы присвоить "id"

        selected_clients = form.cleaned_data['clients']

        for client in selected_clients:
            mailing_settings.clients.add(client)

        form.save_m2m()  # Сохраняем связи многие-ко-многим

        return super().form_valid(form)

class MailingUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')



class MailingDetailView(DetailView):
    model = MailingSettings


class MailingDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')


from django.shortcuts import redirect

class MailingActivateView(UpdateView):
    model = MailingSettings
    form_class = MailingActivateForm
    template_name = 'mailing/mailing_activate.html'

    def form_valid(self, form):
        mailing = form.save(commit=False)
        is_active = form.cleaned_data['is_active']

        if is_active:
            mailing.is_active = True
        else:
            mailing.is_active = False

        mailing.save()

        if mailing.is_active:
            return redirect(reverse('mailing:mailing_detail', kwargs={'pk': mailing.id}))
        else:
            return redirect('mailing:mailing_list')