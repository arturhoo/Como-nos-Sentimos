from django.conf.urls import patterns, include, url
from tastypie.api import Api
from tweets.api import TweetsResource

v1_api = Api(api_name='v1')
v1_api.register(TweetsResource())

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'read_api.views.home', name='home'),
    # url(r'^read_api/', include('read_api.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^read_api/api/', include(v1_api.urls)),
)
