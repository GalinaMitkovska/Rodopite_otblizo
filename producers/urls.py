from django.urls import path
from .views import (
    ProducerListView,
    ProducerDetailView,
    ProducerCreateView,
    ProducerUpdateView,
    ProducerDeleteView,
)

urlpatterns = [
    path('', ProducerListView.as_view(), name='producer-list'),
    path('add/', ProducerCreateView.as_view(), name='producer-add'),
    path('<int:pk>/', ProducerDetailView.as_view(), name='producer-detail'),
    path('<int:pk>/edit/', ProducerUpdateView.as_view(), name='producer-edit'),
    path('<int:pk>/delete/', ProducerDeleteView.as_view(), name='producer-delete'),
]