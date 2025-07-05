from django import forms
from posts import models


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ("title", "content", "description", )

    def __init__(self, *args, **kwargs):
        super(PostCreationForm, self).__init__(*args, **kwargs)
        description_field = self.fields["description"].widget.attrs
        description_field.update({"class": "no-resize",
                                  "rows": 15, })


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ("title", "description", )

    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        description_field = self.fields["description"].widget.attrs
        description_field.update({"class": "no-resize",
                                  "rows": 15, })


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ("content", )

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        content_field = self.fields["content"].widget.attrs
        content_field.update({"class": "no-resize",
                              "rows": 3, })
