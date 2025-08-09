from django.urls import path
from chat.views import MessageListView


urlpatterns = [
    path("<int:user_pk>/", MessageListView.as_view(),
         name="message-list")
]
