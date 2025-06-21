from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    content = models.FileField(upload_to="posts",
                               validators=[FileExtensionValidator(
                                   ["mp4", "jpg", "png", "svg", "vebm",
                                    "gif", "ico", "jpeg"]
                               )])
    title = models.CharField(max_length=455)
    descrption = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name="posts", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ("-created_at", )


class Comment(models.Model):
    content = models.CharField(max_length=1139)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name="comments", null=True)

    def __str__(self):
        return f"{self.author.username} at {self.created_at}"

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ("-changed_at", )


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="likes")

    def __str__(self):
        return f"{self.author.username} - {self.post.title}"

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"


class CommentLike(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name="comment_likes")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                related_name="likes")

    def __str__(self):
        return f"{self.author.username} ({self.comment})"

    class Meta:
        verbose_name = "comment_like"
        verbose_name_plural = "comment_likes"
