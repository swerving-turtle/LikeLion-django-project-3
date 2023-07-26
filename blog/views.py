from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.models import Post


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3
    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, template_name='blog/post_detail.html', context={'post': post})