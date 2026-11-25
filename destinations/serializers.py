from rest_framework import serializers
from .models import Destination


class DestinationSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Destination
        fields = [
            'id',
            'name',
            'category',
            'difficulty',
            'region',
            'description',
            'author_username',
            'created_at',
        ]
        read_only_fields = ['id', 'author_username', 'created_at']