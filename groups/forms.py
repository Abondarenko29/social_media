from django import forms
from groups.models import Group, Article, Media


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("title", "topic", "description", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        description_field = self.fields["description"].widget.attrs
        description_field.update({"id": "markdownify",
                                  "rows": 15,
                                  "class": "no-resize", })


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "content", )

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        content_field = self.fields["content"].widget.attrs
        content_field.update({"class": "no-resize",
                              "id": "markdownify",
                              "rows": 3,
                              "required": "false", })


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ("media", )
