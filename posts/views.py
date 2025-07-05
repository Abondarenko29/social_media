from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts import forms
from posts.models import Tag, Post, Like
from django.contrib import messages
import logging
from posts.mixins import UserIsOwnerMixin
from django.http import HttpResponseRedirect
from django.urls import reverse


logger = logging.getLogger(__name__)


# Create your views here.
class PostCreateView(LoginRequiredMixin, View):
    def post(self, request):
        post_form = forms.PostCreationForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            if not (request.POST.get("tag") in {"", "#", }):
                tags = request.POST.get("tag")
                tags = tags.replace(" ", "")
                tags = tags.replace("\n", "")
                tags = tags.replace(".", "")
                tags = tags.replace(",", "")
                tags = tags.replace("?", "")
                tags = tags.replace("/", "")
                tags = tags.replace("\\", "")
                tags = tags.replace(";", "")
                tags = tags.replace(":", "")
                list_tag = tags.split("#")
                for tag in list_tag:
                    if not (tag in {"", "#", }):
                        Tag.objects.create(name=tag,
                                           post=post)
            messages.success(request, "Post has updated successfuly.")
            return redirect("post-details", pk=post.pk)

        else:
            messages.error(request, post_form.errors)
            context = {
                "post_form": forms.PostCreationForm,
            }
            return render(
                request,
                "posts/post_form.html",
                context
            )

    def get(self, request):
        context = {
            "post_form": forms.PostCreationForm,
            "tags": "",
        }
        return render(
            request,
            "posts/post_form.html",
            context
        )


class PostUpdateView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post_form = forms.PostUpdateForm(request.POST, request.FILES,
                                         instance=post)
        if post_form.is_valid():
            post_form.save()
            Tag.objects.filter(post=post).delete()

            if not (request.POST.get("tag") in {"", "#", }):
                tags = request.POST.get("tag")
                tags = tags.replace(" ", "")
                tags = tags.replace("\n", "")
                tags = tags.replace(".", "")
                tags = tags.replace(",", "")
                tags = tags.replace("?", "")
                tags = tags.replace("/", "")
                tags = tags.replace("\\", "")
                tags = tags.replace(";", "")
                tags = tags.replace(":", "")
                list_tag = tags.split("#")
                for tag in list_tag:
                    if not (tag in {"", "#", }):
                        Tag.objects.create(name=tag,
                                           post=post)
            messages.success(request, "Post has been updated successfuly.")
            return redirect("post-details", pk=pk)

        else:
            messages.error(request, post_form.errors)
            context = {
                "post_form": forms.PostUpdateForm(instance=post),
            }
            return render(
                request,
                "posts/post_form.html",
                context
            )

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        tags = Tag.objects.filter(post=post)
        tags = "#" + " #".join([tag.name for tag in tags])
        context = {
            "post_form": forms.PostUpdateForm(instance=post),
            "tags": tags,
        }
        return render(
            request,
            "posts/post_form.html",
            context
        )

    def get_object(self):
        return Post.objects.get(pk=self.kwargs["pk"])


class PostListView(LoginRequiredMixin, View):
    def get(self, request):
        posts = Post.objects.all()
        context = {"posts": posts, }
        return render(
            request,
            "posts/post_list.html",
            context
        )

    def post(self, request):
        pk = request.POST.get("post")
        slide = request.GET.get("slide")
        if not slide:
            slide = 1
        post = Post.objects.get(pk=pk)
        if not (Like.objects.filter(post=post,
                                    author=request.user)):
            Like.objects.create(author=request.user,
                                post=post)

        else:
            like = Like.objects.get(post=post,
                                    author=request.user)
            like.delete()

        url = reverse("post-list")
        return HttpResponseRedirect(f"{url}?slide={slide}")


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_details.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = forms.CommentForm
        return context

    def post(self, request, pk):
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = self.get_object()
            comment.save()
            messages.success(request,
                             "You have just created a comment.")
        else:
            messages.error(request,
                           comment_form.errors)

        return redirect("post-details", pk=self.kwargs["pk"])


class StreamDetails(LoginRequiredMixin, TemplateView):
    template_name = "posts/stream_details.html"
