from django.urls import path
from chat.views import MessageListView


urlpatterns = [
    path("<int:pk>/", MessageListView.as_view(),
         name="message-list")
]
