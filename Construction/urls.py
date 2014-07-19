from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:    
    url(r'^qms/', include(admin.site.urls)),        
    url(r'^', include('quotes.urls')),    

)
