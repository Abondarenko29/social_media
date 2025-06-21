from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# Create your models here.
class Profile(models.Model):
    class BorderChoices(models.TextChoices):
        YELLOW = "YELLOW", "yellow"
        BLUE = "BLUE", "blue"
        WHITE = "WHITE", "white"

    logo = models.ImageField(upload_to="auth_sys", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    border = models.CharField(max_length=100, choices=BorderChoices.choices,
                              null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(User, related_name="followers",
                                       blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="profile")
    country = CountryField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "profile"
        verbose_name_plural = "profiles"
