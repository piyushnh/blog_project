from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, CreateView, UpdateView,
                                   DeleteView, ListView, DetailView)
from django.urls import reverse_lazy
from .models import Comment, Post
from .forms import  CommentForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import  timezone
from django.contrib.auth.decorators import login_required


# Create your views here.

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    context_object_name = 'my_post'
    model = Post
    template_name = 'blog/post_detail.html'


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    template_name = 'blog/post_form.html'

    model = Post
    form_class = PostForm

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    model = Post
    form_class = PostForm

class PostDeleteView(LoginRequiredMixin, DeleteView):

    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'

    model = Post
    template_name = 'blog/post_draft_list.html'
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

@login_required
def post_publish(request,pk ):
    post = get_object_or_404(Post, pk = pk)
    post.publish()
    # NOTE THAT I HAVE USED POST.PK HERE
    return redirect('blog:post_detail', pk = post.pk)

###########################################################################
# COMMENT MECHANISM STARTS HERE
###########################################################################

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk = pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk = post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    comment.save()
    return redirect('blog:post_detail', pk = comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk = post_pk)
