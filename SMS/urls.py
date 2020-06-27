from django.urls import re_path
from SMS import views

urlpatterns = [
    re_path(r'^send/sms/', views.send_sms),
    re_path(r'^register/', views.register, name='register'),
]
