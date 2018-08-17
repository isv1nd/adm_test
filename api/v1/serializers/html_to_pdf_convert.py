from rest_framework import serializers
from central import models


class URLSerializer(serializers.Serializer):
    url = serializers.URLField(
        required=True, max_length=1024, allow_blank=False, allow_null=False
    )
