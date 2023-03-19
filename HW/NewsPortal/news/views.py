from django.views.generic import ListView, DetailView
from .models import Post
from NewsPortal.settings import BASE_DIR


class PostsList(ListView):
    model = Post  # Модель, объекты которой мы будем выводить
    ordering = '-date'  # поле для сорировки объектов
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = BASE_DIR / 'templates/flatpages/posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = BASE_DIR / 'templates/flatpages/post.html'
    context_object_name = 'post'