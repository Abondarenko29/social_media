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
         name="update-view", )
]
