from django.urls import path
from groups import views


urlpatterns = [
    path("", views.group_list, name="group-list"),
    path("create/", views.GroupCreationView.as_view(),
         name="group-create"),
    path("update/<int:pk>/", views.GroupUpdateView.as_view(),
         name="group-update")
]
