from django.conf.urls import *
from WebPortal.views import archive
from WebPortal.views import getNextHumor
from WebPortal.views import getPrevHumor

urlpatterns = patterns('',
    url(r'^$',archive),
    url(r'^getNextHumor/', getNextHumor),
    url(r'^getPrevHumor/', getPrevHumor),
)
