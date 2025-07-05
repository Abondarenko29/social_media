from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Group(models.Model):
    title = models.CharField(max_length=555)
    topic = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True, related_name="groups_owner")
    members = models.ManyToManyField(User, related_name="groups_member")
    description = models.TextField()

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
    media = models.FileField(upload_to="groups/article")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "article"
        verbose_name_plural = "articles"
