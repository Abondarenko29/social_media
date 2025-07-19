from django.forms import ModelForm
from chat.models import Message, Media


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ("content", )

    def __init__(self):
        content_field = self.fields["content"].widget.attrs
        content_field.update({"rows": 1, "class": ""})


class MediaForm(ModelForm):
    class Meta:
        model = Media
        fields = ("media", )

    def __init__(self):
        media_field = self.fields["media"].widget.attrs
        media_field.update({"class": ""})
