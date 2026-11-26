
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render
from .models import Destination
from .forms import DestinationForm, DestinationUpdateForm
from django.db.models import Q
from .forms import DestinationForm, DestinationUpdateForm, DestinationSearchForm



class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    paginate_by = 6

    def get_queryset(self):
        queryset = Destination.objects.all()

        query = self.request.GET.get('query', '').strip()
        category = self.request.GET.get('category', '')
        sort = self.request.GET.get('sort', 'newest')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(region__icontains=query)
            )

        if category:
            queryset = queryset.filter(category=category)

        if sort == 'name':
            queryset = queryset.order_by('name')
        elif sort == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = DestinationSearchForm(self.request.GET)
        return context


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
    form_class = DestinationUpdateForm
    template_name = 'destinations/destination_update.html'

    def get_queryset(self):
        return Destination.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            'destination-detail',
            kwargs={'pk': self.object.pk}
        )


class DestinationDeleteView(LoginRequiredMixin, DeleteView):
    model = Destination
    template_name = 'destinations/destination_confirm_delete.html'
    success_url = reverse_lazy('destination-list')

    def get_queryset(self):
        return Destination.objects.filter(author=self.request.user)


def home(request):
    return render(request, 'home.html')
