from django.urls import path, re_path
from django.conf.urls import url, include
from web.views import account


urlpatterns = [
    url(r'^register/$', account.register, name='register'),
]
