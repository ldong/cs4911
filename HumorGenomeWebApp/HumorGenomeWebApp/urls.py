from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HumorGenomeWebApp.views.home', name='home'),
    url(r'^WebPortal/', include('WebPortal.urls')),
    url(r'^media(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    url(r'^admin/', include(admin.site.urls)),
)
