from django.conf.urls import *
from WebPortal.views import archive

urlpatterns = patterns('',
    url(r'^$',archive),
)
