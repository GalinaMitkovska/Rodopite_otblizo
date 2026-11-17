from django.urls import path
from .views import (
    AccommodationListView,
    AccommodationDetailView,
    AccommodationCreateView,
    AccommodationUpdateView,
    AccommodationDeleteView,
)

urlpatterns = [
    path('', AccommodationListView.as_view(), name='accommodation_list'),
    path('create/', AccommodationCreateView.as_view(), name='accommodation_create'),
    path('<int:pk>/', AccommodationDetailView.as_view(), name='accommodation_detail'),
    path('<int:pk>/edit/', AccommodationUpdateView.as_view(), name='accommodation_update'),
    path('<int:pk>/delete/', AccommodationDeleteView.as_view(), name='accommodation_delete'),
]