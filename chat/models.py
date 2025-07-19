from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    content = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name="messages", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "message"
        verbose_name_plural = "messages"


# Create your models here.
class Media(models.Model):
    media = models.FileField(upload_to="chat")
    message = models.ForeignKey(Message, on_delete=models.CASCADE,
                                related_name="investments")

    def __str__(self):
        return f"file from {self.message}"

    class Meta:
        verbose_name = "media"
        verbose_name_plural = "media"
