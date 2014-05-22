from django.conf.urls import patterns, url

from tracker import views
from tracker.views import Tracker_View

urlpatterns = patterns('',
    # ex: /tracker/
    url(r'^$', Tracker_View.as_view(), name='tracker_view'),
    # ex: /tracker/bootstrap/
#    url(r'^bootstrap/$', views.bootstrap, name='index-bootstrap'),
    # ex: /tracker/thanks/
    url(r'^thanks/$', views.thanks, name='thanks'),
    # ex: /tracker/5/
    url(r'^(?P<patient_id>\d+)/$', views.detail, name='detail')
)


