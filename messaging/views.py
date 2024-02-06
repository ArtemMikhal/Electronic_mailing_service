from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView

from messaging.forms import MailingMessageForm
from messaging.models import MailingMessage



class MessagingCreateView(CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    template_name = 'messaging/mailingmessage_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        mailing = form.cleaned_data['mailing']

        # Проверка, существует ли уже письмо для выбранной рассылки
        if MailingMessage.objects.filter(mailing=mailing).exists():
            form.add_error('mailing', 'Для этой рассылки письмо уже создано !')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Примените измененную форму
        if form_class is None:
            form.__class__ = MailingMessageForm
        else:
            form.__class__ = form_class
        return form

class MessagingUpdateView(UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:mailing_list')

    


class MessagingDetailView(DetailView):
    model = MailingMessage


class MessagingDeleteView(DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:mailing_list')



