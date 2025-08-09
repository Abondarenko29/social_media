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
        sending_messages = Message.objects.filter(adresat=user)
        getting_messages = Message.objects.filter(adresant=user_pk)
        messages = sending_messages | getting_messages.order_by("created_at")
        context = {
            "user": user,
            "chat_messages": messages,
            "message_form": MessageForm,
            "media_form": MediaForm,
        }

        return render(request,
                      "chat/chat.html",
                      context)

    def post(self, request, user_pk):
        message_form = MessageForm(request.POST)
        media_form = MediaForm(request.POST, request.FILES)
        adresant = User.objects.get(pk=user_pk)

        if media_form.is_valid():
            message = Message.objects.create(adresat=request.user,
                                             adresant=adresant,)
            media = media_form.save(commit=False)
            media.message = message
            media.save()

        elif message_form.is_valid():
            message = message_form.save(commit=False)
            message.adresat = request.user
            message.adresant = adresant
            message.save()

        else:
            messages.error(request, f"Some errors: {message_form.errors}")

        return redirect("message-list", user_pk=user_pk)
