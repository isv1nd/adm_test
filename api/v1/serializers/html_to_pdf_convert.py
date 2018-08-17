from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class URLSerializer(serializers.Serializer):
    url = serializers.URLField(
        required=True, max_length=1024, allow_blank=False, allow_null=False
    )


class HtmlSerializer(serializers.Serializer):
    html_file = serializers.FileField(
        required=True, allow_null=False, allow_empty_file=False
    )

    def validate_html_file(self, value):
        if value.name.split(".")[-1] != "html":
            raise serializers.ValidationError(_("Invalid html file."))
        return value

