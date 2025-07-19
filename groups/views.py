from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from groups.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from groups.forms import GroupForm
from groups.mixins import UserIsOwnerMixin


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
    template_name = "groups/group_form.html"
    form_class = GroupForm
    success_url = reverse_lazy("group-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class GroupUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Group
    template_name = "groups/group_form.html"
    form_class = GroupForm
    success_url = reverse_lazy("group-list")
