
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from .forms import AppUserRegistrationForm, UserProfileUpdateForm
from .models import UserProfile


class RegisterView(CreateView):
    form_class = AppUserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        UserProfile.objects.get_or_create(user=self.object)
        login(self.request, self.object)
        return response


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = 'accounts/edit.html'
    success_url = reverse_lazy('detail')

    def get_object(self, queryset=None):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
