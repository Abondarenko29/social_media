from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from auth_sys.models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "email",)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        email_field = self.fields["email"].widget.attrs
        email_field.update({"required": ""})

        first_name = self.fields["first_name"].widget.attrs
        first_name.update({"required": ""})

        last_name = self.fields["last_name"].widget.attrs
        last_name.update({"required": ""})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("logo", "description", "country", )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        description_field = self.fields["description"].widget.attrs
        description_field.update({"id": "markdownify"})


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        email_field = self.fields["email"].widget.attrs
        email_field.update({"required": ""})

        first_name = self.fields["first_name"].widget.attrs
        first_name.update({"required": ""})

        last_name = self.fields["last_name"].widget.attrs
        last_name.update({"required": ""})
