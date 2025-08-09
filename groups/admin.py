from django.contrib import admin
from groups.models import Group, Article, Like


# Register your models here.
admin.site.register(Group)
admin.site.register(Article)
admin.site.register(Like)
