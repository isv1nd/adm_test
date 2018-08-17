from django.conf import settings
from django.utils import module_loading
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from central.services import exceptions


class URLSerializer(serializers.Serializer):
    url = serializers.URLField(
        required=True, max_length=1024, allow_blank=False, allow_null=False
    )


class HtmlSerializer(serializers.Serializer):
    html_data = serializers.CharField(
        max_length=100000, required=True, allow_blank=False, allow_null=False
    )

    @staticmethod
    def validate_html_data(value):
        html_checker = module_loading.import_string(settings.HTML_CHECKER)()
        try:
            return html_checker.check_html(value)
        except exceptions.InvalidHTML:
            raise serializers.ValidationError(_("Invalid HTML"))
