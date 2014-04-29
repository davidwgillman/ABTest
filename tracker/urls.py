from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',
    # ex: /tracker/5/
    url(r'^$', views.index, name='index'),
    # ex: /tracker/5/
    url(r'^(?P<patient_id>\d+)/$', views.detail, name='detail')
)


