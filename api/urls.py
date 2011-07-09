from django.conf.urls.defaults import *
from tastypie.api import Api
from backend.api import StatesResource, FeelingsResource, SimpleFeelingsResource, UsersResource, TweetsResource

v1_api = Api(api_name='v1')
v1_api.register(StatesResource())
v1_api.register(FeelingsResource())
v1_api.register(SimpleFeelingsResource())
v1_api.register(UsersResource())
v1_api.register(TweetsResource())

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    # Examples:
    # url(r'^$', 'frontend.views.home', name='home'),
    # url(r'^frontend/', include('frontend.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
