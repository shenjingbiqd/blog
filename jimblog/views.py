from django.shortcuts import render, redirect
from .models import Article, ArticleColumn
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.http import HttpResponse
import markdown
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment
from comment.forms import CommentForm


# Create your views here.

def show_article(request):
    posts = Article.objects.all().order_by("-updated")[:5]
    return render(request, "blog/home.html", {'posts': posts})


def show_article_all(request):
    order = request.GET.get('order')
    search = request.GET.get('search')
    column = request.GET.get('column')
    tag = request.GET.get('topic')
    if search:
        posts = Article.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        posts = Article.objects.all()
    if column and column is not None:
        posts = posts.filter(column=column)
    else:
        column = ''
    if tag and tag is not None:
        posts = posts.filter(topic__name__in=[tag])
    else:
        tag = ''
    if order and order is not None:
        if order == 'total_views':
            posts = posts.order_by("-total_views")
    else:
        posts = posts.order_by("-updated")
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, "blog/all.html", {'posts': posts, 'order': order, 'search': search, 'column': column, 'topic': tag})


@login_required(login_url='/user/login/')
def article_create(request):
    if request.user.id == 1:
        if request.method == "POST":
            article_post_form = ArticlePostForm(request.POST, request.FILES)
            if article_post_form.is_valid():
                new_article = article_post_form.save(commit=False)
                new_article.author = User.objects.get(id=request.user.id)
                if request.POST['column'] != 'none':
                    new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
                new_article.save()
                article_post_form.save_m2m()
                return redirect("jimblog:home")
            else:
                return HttpResponse("表单内容有误，请重新填写。")
        else:
            columns = ArticleColumn.objects.all()
            article_post_form = ArticlePostForm()
            context = {'article_post_form': article_post_form, 'columns': columns}
            return render(request, 'blog/article_create.html', context)
    else:
        return HttpResponse('请使用授权用户发表文章')


def article_detail(request, id):
    post = Article.objects.get(id=id)
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
    ])
    post.total_views += 1
    post.save(update_fields=['total_views'])
    comments = Comment.objects.filter(article=id)
    comment_form = CommentForm()
    return render(request, 'blog/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


@login_required(login_url='/user/login/')
def article_modify(request, id):
    post = Article.objects.get(id=id)
    columns = ArticleColumn.objects.all()
    if request.user.id == post.author_id:
        if request.method == 'POST':
            article_post_form = ArticlePostForm(data=request.POST)
            tag = set(request.POST['topic'].split(','))
            tag.discard('')
            tag = list(tag)
            if article_post_form.is_valid():
                post.title = request.POST['title']
                post.body = request.POST['body']
                post.topic.set(*tag, clear=True)
                if request.POST['column'] != 'none':
                    post.column = ArticleColumn.objects.get(id=request.POST['column'])
                post.save()
                return redirect("jimblog:detail", id=post.id)
            else:
                return HttpResponse("数据不合法")
        elif request.method == 'GET':
            article_post_form = ArticlePostForm()
            return render(request, 'blog/modify.html', {'post': post, 'article_post_form': article_post_form, 'columns': columns})
        else:
            return HttpResponse("请使用GET/POST方法")

    else:
        return HttpResponse('请使用授权用户登录')


def article_delete(request, id):
    if request.method == 'POST':
        post = Article.objects.get(id=id)
        post.delete()
        return redirect('jimblog:home')
    else:
        return HttpResponse('请使用POST方法')


def article_column(request):
    columns = ArticleColumn.objects.all()
    return render(request, 'blog/topic.html', {'columns':columns})