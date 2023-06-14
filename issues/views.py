from typing import Optional
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from accounts.models import Role, Team
from .models import Status, Priority, Issue

class IssueCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin, generic.CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["summary", "body", "assignee", "priority", "status"]

    def test_func(self):
        po_role = Role.objects.get(name="product owner")
        return self.request.user.role == po_role

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)
    
class IssueDetailView(generic.DetailView):
    template_name = "issues/detail.html"
    model = Issue

class IssueUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin, generic.UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ["summary", "body", "assignee", "priority", "status"]

    def test_func(self):
        issue = self.get_object()
        return issue.reporter == self.request.user
    
class IssueDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy("issues")

    def test_func(self):
        issue = self.get_object()
        return issue.assignee == self.request.user
    
class IssueListView(generic.ListView):
    template_name = "issues/list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context