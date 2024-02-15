from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog

class BlogListView(ListView):
    model = Blog


class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')
    login_url = reverse_lazy('users:login')
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user

        # Получить файл из формы
        image_file = self.request.FILES.get('image')

        # Если файл присутствует, сохранить его в модели
        if image_file:
            form.instance.image = image_file

        return super().form_valid(form)
class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views +=1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    login_url = reverse_lazy('users:login')
    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        blog = get_object_or_404(Blog, pk=self.kwargs.get('pk'))
        return reverse('blog:view', kwargs={'pk': blog.pk})

class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            raise Http404
        return super().dispatch(request, *args, **kwargs)