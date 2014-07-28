from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^qms/', include(admin.site.urls)),  # noqa
    url(r'^', include('quotes.urls')),

)
