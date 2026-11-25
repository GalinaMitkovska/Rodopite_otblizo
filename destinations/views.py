from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .forms import DestinationForm
from .models import Destination
from django.shortcuts import render


class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    paginate_by = 6


class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destinations/destination_detail.html'
    context_object_name = 'destination'


class DestinationCreateView(LoginRequiredMixin, CreateView):
    model = Destination
    form_class = DestinationForm
    template_name = 'destinations/destination_form.html'
    success_url = reverse_lazy('destination-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DestinationUpdateView(LoginRequiredMixin, UpdateView):
    model = Destination
    form_class = DestinationForm
    template_name = 'destinations/destination_update.html'

    def get_success_url(self):
        return reverse_lazy('destination-detail', kwargs={'pk': self.object.pk})

class DestinationDeleteView(LoginRequiredMixin, DeleteView):
    model = Destination
    template_name = 'destinations/destination_confirm_delete.html'
    success_url = reverse_lazy('destination-list')

def home(request):
    destinations = Destination.objects.all()
    return render(request, 'destinations/destination_list.html', {'destinations': destinations})