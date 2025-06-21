from django.urls import path
from index import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]
