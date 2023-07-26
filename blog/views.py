from django.shortcuts import render, get_object_or_404

from blog.models import Post


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    return render(request, template_name='blog/post_list.html', context={'posts': posts})
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, template_name='blog/post_detail.html', context={'post': post})