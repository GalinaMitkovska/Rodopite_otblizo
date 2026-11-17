from django.urls import path
from .views import (
    DestinationCreateView,
    DestinationDetailView,
    DestinationListView, DestinationUpdateView, DestinationDeleteView,
)

urlpatterns = [
    path('', DestinationListView.as_view(), name='destination-list'),
    path('add/', DestinationCreateView.as_view(), name='destination-add'),
    path('<int:pk>/', DestinationDetailView.as_view(), name='destination-detail'),
    path('<int:pk>/edit/', DestinationUpdateView.as_view(), name='destination-edit'),
    path('<int:pk>/delete/', DestinationDeleteView.as_view(), name='destination-delete'),
]