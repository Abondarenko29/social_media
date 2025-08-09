from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import View, DetailView
from django.urls import reverse_lazy
from groups.models import Group, Article, Like, Media
from django.contrib.auth.mixins import LoginRequiredMixin
from groups.forms import GroupForm
from groups.mixins import UserIsOwnerMixin, UserIsAuthorMixin
from groups import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from groups.decorators import is_article_owner, is_media_owner


# Create your views here.
def group_list(request):
    topic = request.GET.get("topic", "")
    if topic == "":
        groups = Group.objects.all()
        choosed = "All categories"
    else:
        groups = Group.objects.filter(topic=topic)
        choosed = topic
    topics = Group.objects.values('topic')
    topics = set(map(lambda x: tuple(x.values())[0], topics))
    context = {
        "groups": groups,
        "topics": topics,
        "choosed": choosed,
    }
    return render(request,
                  "groups/group_list.html",
                  context)


class GroupCreationView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = "groups/group_creation_form.html"
    form_class = GroupForm
    success_url = reverse_lazy("group-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class GroupUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Group
    template_name = "groups/group_update_form.html"
    form_class = GroupForm
    success_url = reverse_lazy("group-list")


class GroupDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Group
    template_name = "groups/group_delete_form.html"
    success_url = reverse_lazy("group-list")


class ArticleDeleteView(LoginRequiredMixin, UserIsAuthorMixin, View):
    def get_object(self, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs["pk"])
        return article

    def get(self, request, *args, **kwargs):
        context = {
            "pk": self.get_object().group.pk,
        }
        return render(request,
                      "groups/article_delete_form.html",
                      context)

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        article.delete()
        return redirect("group-details", pk=article.group.pk)


class ArticleUpdateView(LoginRequiredMixin, UserIsAuthorMixin, UpdateView):
    model = Article
    form_class = forms.ArticleForm
    template_name = "groups/article_update_form.html"

    def get_success_url(self):
        article = self.get_object().pk
        return reverse_lazy("media-create") + f"?article={article}"


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = "groups/group_details.html"
    context_object_name = "group"


class ArticleCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        parrent_article_pk = request.GET.get("parrent_article")
        group_pk = request.GET.get("group")
        context = {
            "parrent_article_pk": parrent_article_pk,
            "group_pk": group_pk,
            "form": forms.ArticleForm,
        }
        return render(
            request,
            "groups/article_create_form.html",
            context,
        )

    def post(self, request, *args, **kwargs):
        parrent_article_pk = request.POST.get("parrent_article")
        group_pk = request.POST.get("group")
        group = Group.objects.get(pk=group_pk)
        article_form = forms.ArticleForm(request.POST)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.author = request.user
            article.group = group
            if parrent_article_pk != "None":
                parrent_article = Article.objects.get(pk=parrent_article_pk)
                article.parrent_article = parrent_article

            article.save()
            return redirect(reverse_lazy("media-create") +
                            f"?article={article.pk}")

        else:
            context = {
                "parrent_article_pk": parrent_article_pk,
                "group_pk": group_pk,
                "form": forms.ArticleForm,
            }
            messages.error(request, article_form.errors)
            return render(request,
                          "groups/article_create_form.html",
                          context)


@login_required
@is_article_owner
def media_create_view(request, *args, **kwargs):
    if request.method == "POST":
        media = request.FILES.get("media")
        article_pk = request.POST.get("article")
        article = Article.objects.get(pk=article_pk)
        Media.objects.create(media=media,
                             article=article)
        return redirect(reverse_lazy("media-create") +
                        f"?article={article.pk}")

    article_pk = request.GET.get("article")
    article = Article.objects.get(pk=article_pk)
    article_media = Media.objects.filter(article=article)
    context = {
        "article": article_pk,
        "media": article_media,
        "pk": article.group.pk,
    }
    return render(request,
                  "groups/media_create_form.html",
                  context)


@login_required
@is_media_owner
def media_delete_view(request, pk):
    media = Media.objects.get(pk=pk)
    article = media.article
    media.delete()
    return redirect(reverse_lazy("media-create") +
                    f"?article={article.pk}")


@login_required
def article_like_create(request, pk):
    article = Article.objects.get(pk=pk)
    group = article.group

    if not (Like.objects.filter(article=article,
                                author=request.user)):
        Like.objects.create(author=request.user,
                            article=article)

    else:
        like = Like.objects.get(article=article,
                                author=request.user)
        like.delete()

    return redirect("group-details", pk=group.pk)
