from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views

app_name = 'map'

urlpatterns = [
    url(r'^(?P<spot_id>[0-9]+)/delete$', views.delete_reservation, name='delete_reservation'),
    url(r'^(?P<spot_id>[0-9]+)/$', views.reserve, name='reserve'),
    url(r'^login$', views.login_user, name='login_user'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^$', views.map, name='index'),
]
