from django.template import Library
from groups.models import Article, Like
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Model


register = Library()


@register.filter(name="filter")
def filter(model, group):
    if model is None:
        return Article.objects.filter(parrent_article__isnull=True,
                                      group=group)
    return Article.objects.filter(parrent_article=model, group=group)


@register.filter(name="group_paginator")
def group_paginator(model: Model, request):
    paginator = Paginator(model.objects.all(), 1)
    page_num = request.get.GET("page")


@register.filter(name="is_articlelike_author")
def is_like_author(article_pk, user_pk):
    user = User.objects.get(pk=user_pk)
    article = Article.objects.get(pk=article_pk)
    article_obj = Like.objects.filter(article=article, author=user)
    return article_obj.exists()


@register.filter(name="is_image")
def is_image(value):
    if not isinstance(value, str):
        return False
    return value.lower().endswith(("jpg", "png", "svg",
                                   "gif", "ico", "jpeg", ))


@register.filter(name="is_video")
def is_video(value):
    if not isinstance(value, str):
        return False
    return value.lower().endswith(('.mp4', '.webm', ))


@register.filter(name="is_audio")
def is_audio(value):
    if not isinstance(value, str):
        return False
    return value.lower().endswith(('.mp3', '.wav', '.ogg', '.aac'))
