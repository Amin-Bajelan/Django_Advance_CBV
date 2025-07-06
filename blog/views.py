from django.shortcuts import render
from django.views.generic import ListView, TemplateView, RedirectView, DetailView, FormView, CreateView, UpdateView, \
    DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.models import Profile
from blog.models import Post
from django.http import HttpResponse
from .forms import PostForm

from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

class ListPost(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'blog.'
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/list_post.html'
    paginate_by = 2
    ordering = 'id'


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class ListProfile(LoginRequiredMixin, TemplateView):
    template_name = 'blog/list_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profiles'] = Profile.objects.all()
        return context


class RedirectToGoogle(RedirectView):
    url = 'https://www.google.com/'


class DetailPost(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/detail_post.html'
    context_object_name = 'post'


# class CreatePost(LoginRequiredMixin,FormView):
#     template_name = 'blog/create_post.html'
#     form_class = PostForm
#     success_url = '/list/'
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title', 'image', 'content','status', 'published_date']
    form_class = PostForm
    success_url = '/list/'

    def form_valid(self, form):
        form.instance.author = Profile.objects.get(username=self.request.user)
        return super().form_valid(form)


class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = '/list/'


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/list/'


@api_view()
def api_post_list(request):
    return Response({"name":"Amin"})

class ListPostApi(TemplateView):
    template_name = 'blog/list_post_api.html'
