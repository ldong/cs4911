from django.conf.urls import *
from WebPortal.views import *
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^$',archive),
    url(r'^getNextHumor/', getNextHumor),
    url(r'^getPrevHumor/', getPrevHumor),
    url(r'^login', login),
    url(r'^logout', logout),
    url(r'^addContent', addContent),
    url(r'^register', register),
    url(r'^submitRating', submitRating),
<<<<<<< HEAD
    url(r'^resetpassword/passwordsent/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^resetpassword/$', auth_views.password_reset, name='password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^flagContent', flagContent),
    url(r'^getRecommendation/', getRecommendation),
=======
    url(r'^register/', regularuserRegistration),
    url(r'^resetpassword/passwordsent/', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^resetpassword/', auth_views.password_reset, name='password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
    
>>>>>>> a903343075137b35c6e8210dc83f6c07a1328105
)
