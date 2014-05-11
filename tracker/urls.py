from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',
    # ex: /tracker/
    url(r'^$', views.everything_tracker, name='everything_tracker'),
    # ex: /tracker/bootstrap/
#    url(r'^bootstrap/$', views.bootstrap, name='index-bootstrap'),
    # ex: /tracker/thanks/
    url(r'^thanks/$', views.thanks, name='thanks'),
    # ex: /tracker/5/
    url(r'^(?P<patient_id>\d+)/$', views.detail, name='detail')
)


