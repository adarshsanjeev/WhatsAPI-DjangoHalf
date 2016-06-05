"""WhatsAPI URL Configuration"""

from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/profile/$', views.redirect, name='redirect_to_home'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page':'/'}, name='logout'),
    url(r'^accounts/register/$', views.user_register, name="register"),
    url(r'^unread/$', views.get_unread, name='get_unread'),
]
