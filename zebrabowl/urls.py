from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zebrabowl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'apps.scorecard.views.new_game', name='roothome'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^scorecard/',include('apps.scorecard.urls')),
    (r'^accounts/', include('userena.urls')),
)
