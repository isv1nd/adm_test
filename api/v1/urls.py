from django.conf import urls

from api.v1.views import html_to_pdf_convert

urlpatterns = [
    urls.url(
        'convert_html_to_pdf/link/',
        html_to_pdf_convert.ConvertHtmlToPdfUsingLinkView.as_view(),
        name='v1_convert_html_to_pdf_link'
    ),
    urls.url(
        'convert_html_to_pdf/data/',
        html_to_pdf_convert.ConvertHtmlToPdfUsingHtmlDataView.as_view(),
        name='v1_convert_html_to_pdf_data'
    ),
]
