from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.wav_list_view, name='list'),
    url(r'^add/$', views.wav_add_view, name='add'),
    url(r'^change/(?P<pk>[0-9]+)/$', views.wav_change_view, name='change'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.wav_delete_view, name='delete')
]
