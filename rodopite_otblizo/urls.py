from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from destinations.api_views import DestinationListCreateAPIView
from destinations import views as destination_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", destination_views.home, name="home"),
    path('accounts/', include('accounts.urls')),
    path('destinations/', include('destinations.urls')),
    path('producers/', include('producers.urls')),
    path('accommodations/', include('accommodations.urls')),
    path('community/', include('community.urls')),
    path('api/destinations/', DestinationListCreateAPIView.as_view(), name='api-destinations'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)