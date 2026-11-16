from django.urls import path
from .views import ProducerCreateView, ProducerDetailView, ProducerListView

urlpatterns = [
    path('', ProducerListView.as_view(), name='producer-list'),
    path('<int:pk>/', ProducerDetailView.as_view(), name='producer-detail'),
    path('add/', ProducerCreateView.as_view(), name='producer-add'),
]