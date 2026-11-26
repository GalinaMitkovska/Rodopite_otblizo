
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .forms import ProducerForm
from .models import Producer


class ProducerListView(ListView):
    model = Producer
    template_name = 'producers/producer_list.html'
    context_object_name = 'producers'


class ProducerDetailView(DetailView):
    model = Producer
    template_name = 'producers/producer_detail.html'
    context_object_name = 'producer'


class ProducerCreateView(LoginRequiredMixin, CreateView):
    model = Producer
    form_class = ProducerForm
    template_name = 'producers/producer_form.html'
    success_url = reverse_lazy('producer-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProducerUpdateView(LoginRequiredMixin, UpdateView):
    model = Producer
    form_class = ProducerForm
    template_name = 'producers/prodicer_update.html'

    def get_queryset(self):
        return Producer.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('producer-detail', kwargs={'pk': self.object.pk})


class ProducerDeleteView(LoginRequiredMixin, DeleteView):
    model = Producer
    template_name = 'producers/producer_confirm_delete.html'
    success_url = reverse_lazy('producer-list')

    def get_queryset(self):
        return Producer.objects.filter(owner=self.request.user)


