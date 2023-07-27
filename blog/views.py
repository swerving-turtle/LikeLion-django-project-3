from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from blog.models import Post
from django.core.mail import send_mail
from blog.forms import EmailPostForm, CommentForm


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
    form = CommentForm()
    comments = post.comments.filter(active=True)
    return render(request, template_name='blog/post_detail.html', context={'post': post, 'form': form, 'comments': comments})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['name']} 님이 {post.title}을(를) 추천합니다."
            message = f"{post.title}을 {post_url}에서 읽어보세요.\n\n" \
                      f"{data['name']}님의 의견: {data['comments']}"
            send_mail(subject, message, '', [data['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post_share.html', {'post': post, 'form': form, 'sent': sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    comments = post.comments.filter(active=True)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(post)

    return render(request, 'blog/post/detail.html', {'post': post, 'form': form, 'comments': comments})