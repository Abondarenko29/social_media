from django import forms
from groups.models import Group


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
