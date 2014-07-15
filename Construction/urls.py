from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Construction.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^qms/', include(admin.site.urls)),        
    url(r'^', include('quotes.urls')),    

)
