from django import template
from posts.models import Comment, Post, Like, CommentLike
from django.contrib.auth.models import User

register = template.Library()


@register.filter(name="filter")
def filter(model, post):
    if model is None:
        return Comment.objects.filter(replied_comment__isnull=True,
                                      post=post)
    return Comment.objects.filter(replied_comment=model, post=post)


@register.filter(name="is_like_author")
def is_like_author(post_pk, user_pk):
    user = User.objects.get(pk=user_pk)
    post = Post.objects.get(pk=post_pk)
    comment_obj = Like.objects.filter(post=post, author=user)
    return comment_obj.exists()


@register.filter(name="is_commentlike_author")
def is_commentlike_author(comment_pk, user_pk):
    user = User.objects.get(pk=user_pk)
    comment = Comment.objects.get(pk=comment_pk)
    comment_obj = CommentLike.objects.filter(comment=comment, author=user)
    return comment_obj.exists()


@register.filter(name="endswith")
def endswith(value, arg):
    if not isinstance(value, str):
        return False
    return value.lower().endswith(arg.lower())


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
