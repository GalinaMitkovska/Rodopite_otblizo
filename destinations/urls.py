from django.urls import path
from .views import (
    DestinationCreateView,
    DestinationDetailView,
    DestinationListView,
)

urlpatterns = [
    path('', DestinationListView.as_view(), name='destination-list'),
    path('add/', DestinationCreateView.as_view(), name='destination-add'),
    path('<int:pk>/', DestinationDetailView.as_view(), name='destination-detail'),
]