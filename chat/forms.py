from django.forms import ModelForm
from chat.models import Message, Media


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ("content", )

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        content_field = self.fields["content"].widget.attrs
        content_field.update({"rows": 2, "class": "no-resize"})


class MediaForm(ModelForm):
    class Meta:
        model = Media
        fields = ("media", )

    def __init__(self, *args, **kwargs):
        super(MediaForm, self).__init__(*args, **kwargs)

        media_field = self.fields["media"].widget.attrs
        media_field.update({"class": ""})
