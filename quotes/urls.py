from django.conf.urls import patterns, url
from quotes import views

urlpatterns = patterns('',
	#Main Index page - Ex: /
	url(r'^$', views.Index, name='index'),
    #Design Selector
    url(r'^(\d+)/$', views.Design, name='designs'),
    #Quotes viewing page
	url(r'^quote/$', views.Quote, name='quote'),
)