from django.conf.urls import patterns, url
from quotes import views

urlpatterns = patterns('',
	#Main Index page - Ex: /
	url(r'^$', views.Index, name='index'),
    #Services page - Static Template - Ex: /construction
    url(r'^services/$', views.Services, name='services'),
    #About us page - Static Template - Ex: /aboutus
    url(r'^aboutus/$', views.AboutUs, name='aboutus'),    
    #Quotes submission URLS
	url(r'^quote/$', views.SubmitQuote, name='quote'),
    url(r'^thanks/$', views.Thanks, name='thanks'),    
    #Quotes Management System URLS
    url(r'^exportqms/$', views.Export, name='export'),
    url(r'^exportqms/ToXLS/', views.ExportToXLS, name='exportXLS')
)