"""WhatsAPI URL Configuration"""

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login/$', views.user_login, name="login"),
    url(r'^register/$', views.user_register, name="register"),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^unread/$', views.get_unread, name='get_unread'),
]
