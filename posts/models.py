from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.
class Post(models.Model):
    content = models.FileField(upload_to="posts",
                               validators=[FileExtensionValidator(
                                   ["mp4", "jpg", "png", "svg", "webm",
                                    "gif", "ico", "jpeg", ]
                               )])
    title = models.CharField(max_length=455)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name="posts", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ("-created_at", )


class Stream(models.Model):
    name = models.CharField(max_length=455)
    descrption = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name="streams", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "stream"
        verbose_name_plural = "streams"
        ordering = ("-created_at", )


class Tag(models.Model):
    name = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="tags", null=True, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE,
                               related_name="tags", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not (self.post or self.stream):
            raise ValidationError("tag must have an foreign key.")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"


class Connection(models.Model):
    channel_name = models.CharField(max_length=500)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE,
                               related_name="connections")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="connections")
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    metadata = models.JSONField()

    class Meta:
        verbose_name = "connection"
        verbose_name_plural = "connections"

    def __str__(self):
        return self.channel_name


class Comment(models.Model):
    content = models.CharField(max_length=1139)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name="comments", null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments", null=True, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE,
                               related_name="comments", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not (self.post or self.stream):
            raise ValidationError("tag must have an foreign key.")
        return super().save(*args, **kwargs)

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
                             related_name="likes", null=True, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE,
                               related_name="likes", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not (self.post or self.stream):
            raise ValidationError("tag must have an foreign key.")
        return super().save(*args, **kwargs)

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


class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name="ratings")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="rating")
    value = models.FloatField(validators=[MaxValueValidator(10)])

    def __str__(self):
        return f"{self.author} - {self.value}⭐."

    class Meta:
        verbose_name = "rating"
        verbose_name_plural = "rating"
