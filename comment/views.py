from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from jimblog.models import Article
from .forms import CommentForm


# Create your views here.
@login_required(login_url='/user/login/')
def comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse('表单内容有误')

    else:
        return HttpResponse("发表评论仅接受POST请求")


