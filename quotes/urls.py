from django.conf.urls import patterns, url
from quotes import views

urlpatterns = patterns('',
	#Main Index page - Ex: /
	url(r'^$', views.Index, name='index'),        
    #Quotes viewing page
	url(r'^quote/$', views.SubmitQuote, name='quote'),
    url(r'^thanks/$', views.Thanks, name='quote'),
    #Quotes submission page
    #Quotes Management System URLS
    url(r'^exportqms/$', views.Export, name='export'),
    url(r'^exportqms/ToXLS/', views.ExportToXLS, name='exportXLS')
)