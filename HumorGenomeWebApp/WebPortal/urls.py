from django.conf.urls import *
from WebPortal.views import *

urlpatterns = patterns('',
    url(r'^$',archive),
    url(r'^getNextHumor/', getNextHumor),
    url(r'^getPrevHumor/', getPrevHumor),
    url(r'^login', login),
    url(r'^logout', logout),
    url(r'^submitRating', submitRating),
)
