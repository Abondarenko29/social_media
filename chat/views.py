from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from chat.models import Message
from chat.forms import MessageForm, MediaForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# Create your views here.
class MessageListView(LoginRequiredMixin, View):
    def get(self, request, user_pk):
        user = User.objects.get(pk=user_pk)
        context = {
            "messages": Message.objects.filter(author=user)
        }

        return render(request,
                      "chat/chat.html",
                      context)

    def post(self, request, pk):
        message_form = MessageForm(request.POST)
        media_form = MediaForm(request.POST)

        if media_form.is_valid():
            message = message_form.save(commit=False)
            message.author = request.user
            media = media_form.save(commit=False)
            media.message = message
            message.save()
            media.save()

        elif media_form.is_valid():
            message = media_form.save(commit=False)
            message.author = request.user
            message.save()

        else:
            messages.error(f"Some errors: {message_form.errors}")

        return redirect("message-list", pk=pk)
