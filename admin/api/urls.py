from django.urls import path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api.views import YouTuberViewSet
                                        

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='swagger-ui', permanent=False)),

    # Swagger and schema
    path('doc', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema', SpectacularAPIView.as_view(), name='schema'),

    path('youtubers', YouTuberViewSet.as_view({'get': 'list', 'post': 'create'}), name='youtubers'),
    path('youtuber/<int:pk>', YouTuberViewSet.as_view({'get': 'retrieve', 'patch': 'update'}), name='youtubers'),
]
