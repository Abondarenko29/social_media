from django.shortcuts import render, redirect
from django.views.generic import View, DeleteView, DetailView
from auth_sys import forms
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from auth_sys.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User


# Create your views here.
class RegisterView(View):
    def post(self, request):
        user_form = forms.CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect("profile-update")
        else:
            messages.error(request, user_form.errors)
            self.context = {"user_form": forms.CustomUserCreationForm,
                            "profile_form": forms.ProfileForm, }
            return render(
                request,
                "auth_sys/register_form.html",
                self.context
            )

    def get(self, request):
        self.context = {"user_form": forms.CustomUserCreationForm, }
        return render(
            request,
            "auth_sys/register_form.html",
            self.context
        )


class CustomLoginView(LoginView):
    template_name = "auth_sys/login_form.html"
    success_url = reverse_lazy("home")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "auth_sys/profile_update_form.html"

    def post(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        profile_form = forms.ProfileForm(request.POST, request.FILES,
                                         instance=profile)

        if profile_form.is_valid():
            updated_profile = profile_form.save(commit=False)
            updated_profile.user = user
            updated_profile.save()
            login(request, user)
            return redirect("home")
        else:
            context = {
                "profile_form": forms.ProfileForm(instance=self.profile),
            }
            messages.error(request, profile_form.errors)

            return render(request,
                          self.template_name,
                          context)

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)

        context = {
            "profile_form": forms.ProfileForm(instance=profile),
        }
        return render(request,
                      self.template_name,
                      context)


class UserUpdateView(LoginRequiredMixin, View):
    template_name = "auth_sys/user_update_form.html"

    def post(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)

        user_form = forms.UserUpdateForm(request.POST, instance=user)
        profile_form = forms.ProfileForm(request.POST, request.FILES,
                                         instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            updated_user = user_form.save()
            updated_profile = profile_form.save(commit=False)
            updated_profile.user = updated_user
            updated_profile.save()
            login(request, updated_user)
            return redirect("home")
        else:
            context = {
                "user_form": forms.UserUpdateForm(instance=self.user),
                "profile_form": forms.ProfileForm(instance=self.profile),
            }
            messages.error(request, user_form.errors)
            messages.error(request, profile_form.errors)

            return render(request,
                          self.template_name,
                          context)

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)

        context = {
            "user_form": forms.UserUpdateForm(instance=user),
            "profile_form": forms.ProfileForm(instance=profile),
        }
        return render(request,
                      self.template_name,
                      context)


class UserPasswordUpdateView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy("news_list")
    template_name = "auth_sys/user_password_update_form.html"


class CustomUserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "auth_sys/user_delete_form.html"
    success_url = reverse_lazy("register")

    def get_object(self, queryset=None):
        return self.request.user


class UserDetails(DetailView):
    template_name = "auth_sys/user_details.html"
    model = User
    context_object_name = "user"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.get_object()
        profile = Profile.objects.get(user=user)
        context["profile"] = profile
        return context


def follow(request, pk):
    user = User.objects.get(pk=pk)
    if user != request.user:
        if not (request.user in user.profile.followers.all()):
            user.profile.followers.add(request.user)
        else:
            user.profile.followers.remove(request.user)

        return redirect("user-details", pk=pk)
    else:
        raise BaseException("You can't follow yourself.")
