from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Group(models.Model):
    title = models.CharField(max_length=555)
    topic = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True, related_name="groups_owner")
    members = models.ManyToManyField(User, related_name="groups_member")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "group"
        verbose_name_plural = "groups"


class Article(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name="articles")
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, related_name="articles")
    title = models.CharField(max_length=255)
    content = models.TextField()
    parrent_article = models.ForeignKey("self", on_delete=models.CASCADE,
                                        related_name="dother_articles",
                                        null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "article"
        verbose_name_plural = "articles"


class Media(models.Model):
    media = models.FileField(upload_to="groups/articles/")
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name="media")

    def __str__(self):
        return self.media.name

    class Meta:
        verbose_name = "media"
        verbose_name_plural = "media"


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name="post_likes")
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name="likes")

    def __str__(self):
        return f"{self.author.username} - {self.article.title}"

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"
