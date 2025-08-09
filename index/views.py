from django.shortcuts import render
from django.views.generic import ListView
from posts.models import Post
from django.contrib.postgres.search import SearchVector, SearchQuery
from auth_sys.models import Profile


# Create your views here.
class HomeView(ListView):
    template_name = "index/home.html"
    model = Post
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Post.objects.none()
        if self.request.user.is_authenticated:
            profiles = Profile.objects.filter(
                                              followers__in=[self.request.user.id])
            for follower in profiles:
                queryset.union(Post.objects.filter(author=follower.user))

            context["posts"] = queryset

        return context


def search_view(request):
    query = request.GET.get("q", "")
    results = Post.objects.annotate(
        search=SearchVector('title', 'description')
    ).filter(search=SearchQuery(query))

    context = {
        "posts": results,
    }
    return render(request, "index/home.html", context)


def close_page(request):
    return render(request,
                  "index/close_page.html",
                  {})
