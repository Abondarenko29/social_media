from groups.models import Article, Media
from django.core.exceptions import PermissionDenied


def is_article_owner(func):
    def wrapper(request, *args, **kwargs):
        if request.method == "GET":
            pk = request.GET.get("article")
            article = Article.objects.get(pk=pk)

        elif request.method == "POST":
            pk = request.POST.get("article")
            article = Article.objects.get(pk=pk)

        if request.user != article.author:
            raise PermissionDenied
        return func(request, *args, **kwargs)

    return wrapper


def is_media_owner(func):
    def wrapper(request, *args, **kwargs):
        pk = kwargs["pk"]
        article = Media.objects.get(pk=pk).article

        if request.user != article.author:
            raise PermissionDenied
        return func(request, *args, **kwargs)

    return wrapper
