from rest_framework import serializers

from api.models import YouTuber


class YouTuberSerializer(serializers.ModelSerializer):

    class Meta:
        model = YouTuber
        fields = "__all__"

