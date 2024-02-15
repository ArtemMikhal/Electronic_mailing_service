from django.db.models import Count

from blog.models import Blog

from django.views.generic import TemplateView
from mailing.models import MailingSettings, Client


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение общего количества рассылок
        total_mailings = MailingSettings.objects.count()

        # Получение количества активных рассылок
        active_mailings = MailingSettings.objects.filter(is_active=True).count()

        # Получение количества уникальных клиентов для рассылок
        unique_clients = Client.objects.annotate(num_mailings=Count('mailingsettings')).filter(num_mailings=0).count()

        context['total_mailings'] = total_mailings
        context['active_mailings'] = active_mailings
        context['unique_clients'] = unique_clients

        # Получение трех случайных статей из блога
        random_blogs = Blog.objects.order_by('?')[:3]
        context['random_blogs'] = random_blogs

        return context
