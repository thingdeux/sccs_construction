from django.conf.urls import patterns, url
from quotes import views

urlpatterns = patterns('',
	#Main Index page - Ex: /
	url(r'^$', views.Index, name='index'),    
    #url(r'robots\.txt$')
    #Quotes viewing page
	url(r'^quote/$', views.ViewQuote, name='quote'),
    url(r'^exportqms/$', views.Export, name='export'),
    url(r'^exportqms/ToXLS/', views.ExportToXLS, name='exportXLS')
)