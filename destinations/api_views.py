from rest_framework import generics, permissions
from .models import Destination
from .serializers import DestinationSerializer


class DestinationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DestinationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Destination.objects.select_related('author').all()
        region = self.request.query_params.get('region')
        category = self.request.query_params.get('category')
        if region:
            queryset = queryset.filter(region__icontains=region)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)