from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Goal


class GoalList(ListView):
    model = Goal
    context_object_name = 'goals'
    template_name = 'list_goals.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goals'] = context['goals'].filter(user=self.request.user)
        return context


class GoalDetailView(DetailView):
    model = Goal
    template_name = 'goal_detail.html'
    context_object_name = 'goal'
