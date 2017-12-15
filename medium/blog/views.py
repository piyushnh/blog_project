from django.shortcuts import render
from django.views.generic import (TemplateView, CreateView, UpdateView,
                                   DeleteView, ListView, DetailView)
from django.urls import reverse_lazy
from .models import Comment, Post
from .form import  CommentForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import  timezone


# Create your views here.

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects,filter(published_date__lte = timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = post

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = /login/
    redirect_field_name = 'blog/post_detail.html'

    model = Post
    form_class = PostForm

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = /login/
    redirect_field_name = 'blog/post_detail.html'

    model = Post
    form_class = PostForm

class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = /login/
    # not sure of adding this field.Experimentation
    redirect_field_name = 'blog/post_list.html'

    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')
