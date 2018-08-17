from rest_framework import serializers
import bs4


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
        """This validation is just example. Html validation is a
        little bit more complex process.
        """
        if not bs4.BeautifulSoup(value, "html.parser").find("html"):
            raise serializers.ValidationError("Invalid HTML")
        return value
