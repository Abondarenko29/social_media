from django.urls import path
from auth_sys import views


urlpatterns = [
    path("register/", views.RegisterView.as_view(),
         name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("update/", views.UserUpdateView.as_view(), name="user-update"),
    path("update/password/", views.UserPasswordUpdateView.as_view(),
         name="user-update-password"),
    path("delete/", views.CustomUserDeleteView.as_view(), name="user-delete"),
    path("<int:pk>/", views.UserDetails.as_view(), name="user-details"),
    path("register/profile/", views.ProfileUpdateView.as_view(),
         name="profile-update"),
    path("<int:pk>/follow/", views.follow, name="follow")
]
