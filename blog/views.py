from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import DetailView
from blog.models import Post


class PostDetailView(DetailView):
    model = Post


def news(request):
    posts = Post.objects.all()
    return render(request, 'blog/news.html', {'object_list': posts})