from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import TravelStory
from .forms import TravelStoryForm


class StoryListView(ListView):
    model = TravelStory
    template_name = 'community/story_list.html'
    context_object_name = 'stories'
    paginate_by = 6


class StoryDetailView(DetailView):
    model = TravelStory
    template_name = 'community/story_detail.html'
    context_object_name = 'story'


class StoryCreateView(LoginRequiredMixin, CreateView):
    model = TravelStory
    form_class = TravelStoryForm
    template_name = 'community/story_form.html'
    success_url = reverse_lazy('story_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class StoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TravelStory
    form_class = TravelStoryForm
    template_name = 'community/story_form.html'

    def test_func(self):
        story = self.get_object()
        return self.request.user == story.author

    def get_success_url(self):
        return reverse_lazy('story_detail', kwargs={'pk': self.object.pk})


class StoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TravelStory
    template_name = 'community/story_confirm_delete.html'
    success_url = reverse_lazy('story_list')

    def test_func(self):
        story = self.get_object()
        return self.request.user == story.author


@login_required
def like_story(request, pk):
    story = get_object_or_404(TravelStory, pk=pk)
    if request.user in story.likes.all():
        story.likes.remove(request.user)
    else:
        story.likes.add(request.user)
    return redirect('story_detail', pk=pk)