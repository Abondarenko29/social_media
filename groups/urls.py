from django.urls import path
from groups import views


urlpatterns = [
    path("", views.group_list, name="group-list"),
    path("create/", views.GroupCreationView.as_view(),
         name="group-create"),
    path("update/<int:pk>/", views.GroupUpdateView.as_view(),
         name="group-update"),
    path("<int:pk>/", views.GroupDetailView.as_view(),
         name="group-details"),
    path("delete/<int:pk>/", views.GroupDeleteView.as_view(),
         name="group-delete"),
    path("like/<int:pk>/", views.article_like_create,
         name="article-like-create"),
    path("article/update/<int:pk>/", views.ArticleUpdateView.as_view(),
         name="article-update"),
    path("article/delete/<int:pk>/", views.ArticleDeleteView.as_view(),
         name="article-delete"),
    path("article/create/", views.ArticleCreateView.as_view(),
         name="article-create"),
    path("article/media", views.media_create_view,
         name="media-create"),
    path("article/media/<int:pk>/delete", views.media_delete_view,
         name="media-delete"),
]
