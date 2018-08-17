from django.conf import urls


urlpatterns = [
    urls.url('v1/', urls.include('api.v1.urls')),
]
