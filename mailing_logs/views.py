from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView

from mailing_logs.models import MailingLog


class MailingLogsListView(LoginRequiredMixin, ListView):
    model = MailingLog
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        queryset = super().get_queryset()
        # Фильтруем список логов по рассылкам, созданным текущим пользователем
        queryset = queryset.filter(mailing__user=self.request.user)
        return queryset