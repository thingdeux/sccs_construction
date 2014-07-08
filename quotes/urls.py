from django.conf.urls import patterns, url
from quotes import views

urlpatterns = patterns('',
	#Main Index page
	url(r'^$', views.Index, name='index'),
    #Quotes viewing page
	url(r'^quote/$', views.Quote, name='quote'),
)