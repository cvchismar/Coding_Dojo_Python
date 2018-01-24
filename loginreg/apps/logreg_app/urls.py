from django.conf.urls import url
from . import views
urlpatterns = [
        url(r'^$', views.index, name="index"),
        url(r'^register$', views.register),
        url(r'^display$', views.display, name="display"),
        url(r'^login$', views.login),
        url(r'^add$', views.add, name="add"),
        url(r'^create$', views.create, name="create"),
        #url(r'^show$', views.show, name='show'),
        url(r'^info$', views.create, name="info"),
        url(r'^join/(?P<trip_id>\d+)$', views.join, name='join'),
        url(r'^leave/(?P<trip_id>\d+)$', views.leave, name='leave'),
        url(r'^info/(?P<trip_id>\d+)$', views.info, name='info'),
        url(r'^logout$', views.logout, name="logout"),
]