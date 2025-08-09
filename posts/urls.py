from django.urls import path
from posts import views


urlpatterns = [
    path("create/", views.PostCreateView.as_view(),
         name="post-create"),
    path("view/", views.PostListView.as_view(),
         name="post-list"),
    path("stream/", views.StreamDetails.as_view(),
         name="stream_details"),
    path("<int:pk>/", views.PostDetailView.as_view(),
         name="post-details"),
    path("update/<int:pk>/", views.PostUpdateView.as_view(),
         name="post-update"),
    path("<int:pk>/comment/like/", views.comment_like_create,
         name="comment-like-create"),
    path("<int:pk>/like/", views.like_create,
         name="like-create"),
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view(),
         name="comment-update"),
    path("comment/<int:pk>/delete", views.CommentDeleteView.as_view(),
         name="comment-delete"),
]
