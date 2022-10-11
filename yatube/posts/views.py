from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)
from django.views.decorators.cache import cache_page

from core.paginator import paginator

from posts.forms import CommentForm, PostForm
from posts.models import Comment, Follow, Group, Post, User


# а в шаблоне тогда не надо кешировать?
@cache_page(20)
def index(request):
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    post_list = Post.objects.select_related('author', 'group')
    page_obj = paginator(request, post_list)

    context = {
        'title': title,
        'page_obj': page_obj
    }
    return render(request, template, context)


def group_posts(request, slug: str):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    title = f'Записи сообщества {group}'
    post_list = group.posts.select_related('author')
    page_obj = paginator(request, post_list)

    context = {
        'group': group,
        'title': title,
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username: str):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    author_posts = author.posts.select_related('author')
    amount = author_posts.count()
    following = author.following.all()
    title = f'Все посты пользователя {author}'
    page_obj = paginator(request, author_posts)

    context = {
        'author': author,
        'amount': amount,
        'following': following,
        'title': title,
        'page_obj': page_obj
    }
    return render(request, template, context)


def post_detail(request, post_id: int):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    amount = post.author.posts.count()
    is_edit = post.author == request.user
    comment_form = CommentForm()
    comments = Comment.objects.select_related('post')

    context = {
        'post': post,
        'amount': amount,
        'is_edit': is_edit,
        'form': comment_form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    group_list = Group.objects.all()

    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    context = {
        'form': form,
        'group_list': group_list
    }
    if not form.is_valid():
        return render(request, template, context)

    new_post = form.save(commit=False)
    new_post.author = request.user
    new_post.save()
    return redirect('posts:profile', new_post.author)


@login_required
def post_edit(request, post_id: int):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    group_list = Group.objects.all()
    is_edit = True

    if post.author != request.user:
        return redirect('posts:post_detail', post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    context = {
        'form': form,
        'post': post,
        'group_list': group_list,
        'is_edit': is_edit
    }
    if not form.is_valid():
        return render(request, template, context)

    form.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    # информация о текущем пользователе доступна в переменной request.user
    template = 'posts/follow.html'
    post_list = Post.objects.filter(author__following__user=request.user)
    title = 'Подписки'
    page_obj = paginator(request, post_list)

    context = {
        'title': title,
        'page_obj': page_obj
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    # Подписаться на автора
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(
            author=author,
            user=request.user
        )
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    # Отписаться от автора
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(author=author, user=request.user).delete()
    return redirect('posts:profile', username)
