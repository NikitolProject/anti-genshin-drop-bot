from __future__ import annotations

from datetime import datetime

from drf_spectacular.utils import OpenApiParameter, extend_schema

from rest_framework import permissions, viewsets

from rest_framework.generics import (
    CreateAPIView, 
    DestroyAPIView,
    UpdateAPIView, 
    RetrieveAPIView,
    ListAPIView
)
from rest_framework.response import Response

from api.serializers import YouTuberSerializer

from api.models import YouTuber


class YouTuberViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = YouTuberSerializer
    queryset = YouTuber.objects.all()

    def get_queryset(self) -> YouTuber:
        url = self.request.query_params.get('url')

        if url:
            return YouTuber.objects.filter(url=url)
        
        return YouTuber.objects.all()
