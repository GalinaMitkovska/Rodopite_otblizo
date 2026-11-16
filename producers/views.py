
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
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