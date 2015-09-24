from django.conf.urls import url

from . import views

# REST example
from django.conf.urls import include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'roadcar', views.RoadcarViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^$', views.IndexView.as_view(), name='index'),  replaced by previous string
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^ajaxexample$', views.main),
    url(r'^ajaxexample_json$', views.ajax),
    url(r'^real-time$', views.realtime),
    url(r'^get-real-time$', views.getrealtime, name='getrealtime'),
    # REST example
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
