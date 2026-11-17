
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Accommodation
from .forms import AccommodationForm


class AccommodationListView(ListView):
    model = Accommodation
    template_name = 'accommodations/accommodation_list.html'
    context_object_name = 'accommodations'
    paginate_by = 6  # По желание: разделяне на страници


class AccommodationDetailView(DetailView):
    model = Accommodation
    template_name = 'accommodations/accommodation_detail.html'
    context_object_name = 'accommodation'


class AccommodationCreateView(LoginRequiredMixin, CreateView):
    model = Accommodation
    form_class = AccommodationForm
    template_name = 'accommodations/accommodation_form.html'
    success_url = reverse_lazy('accommodation_list')

    def form_valid(self, form):
        # Автоматично задаване на текущия потребител за собственик
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AccommodationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Accommodation
    form_class = AccommodationForm
    template_name = 'accommodations/accommodation_form.html'

    def test_func(self):
        # Само собственикът може да редактира мястото
        accommodation = self.get_object()
        return self.request.user == accommodation.owner

    def get_success_url(self):
        return reverse_lazy('accommodation_detail', kwargs={'pk': self.object.pk})


class AccommodationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Accommodation
    template_name = 'accommodations/accommodation_confirm_delete.html'
    success_url = reverse_lazy('accommodation_list')

    def test_func(self):
        # Само собственикът може да изтрие мястото
        accommodation = self.get_object()
        return self.request.user == accommodation.owner