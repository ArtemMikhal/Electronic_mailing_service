from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from customers.forms import ClientForm
from customers.models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        queryset = super().get_queryset()
        # Фильтруем список клиентов по текущему пользователю
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'customers/client_form.html'
    success_url = reverse_lazy('customers:list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('customers:list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.user = self.get_object().user
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    login_url = reverse_lazy('users:login')

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('customers:list')
    login_url = reverse_lazy('users:login')