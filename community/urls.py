from django.urls import path
from .views import (
    StoryListView,
    StoryDetailView,
    StoryCreateView,
    StoryUpdateView,
    StoryDeleteView,
    like_story,
)

urlpatterns = [
    path('', StoryListView.as_view(), name='story_list'),
    path('create/', StoryCreateView.as_view(), name='story_create'),
    path('<int:pk>/', StoryDetailView.as_view(), name='story_detail'),
    path('<int:pk>/edit/', StoryUpdateView.as_view(), name='story_update'),
    path('<int:pk>/delete/', StoryDeleteView.as_view(), name='story_delete'),
    path('<int:pk>/like/', like_story, name='story_like'),
]