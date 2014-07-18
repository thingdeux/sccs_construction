from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.core import serializers
from django import forms
from quotes.models import Quote

def Export_Selected(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/exportqms/?ct=%s&ids=%s" % (ct.pk, ",".join(selected))) 

def CloseQuote(modeladmin, request, queryset):
    queryset.update(closed="True")
CloseQuote.short_description = "Close Quote"


class ClosedQuoteFilter(admin.SimpleListFilter):
    #Title displayed in the admin sidebar/topbar
    title = "Quote Closed?"
    parameter_name = 'Status'

    def lookups(self, request, model_admin):
        #List of tuples, the 2nd element is the readable name in the UI
        return (
            ('Closed', ('Closed Quotes')),
            ('Open', ('Open Quotes')),
            ('All', ('All Quotes')),
        )

    def queryset(self, request, queryset):        
        #Filtered queryset based on the value provided in querystring
        if self.value() == 'Closed':            
            return queryset.filter(closed=True)
        if self.value() == 'Open':
            return queryset.filter(closed=False)
        #By Default only open quotes show
        if self.value() == "All":
            return queryset.all()
        if self.value() == None:            
            return queryset.filter(closed=False)

class QuoteAdmin(admin.ModelAdmin):    
    ordering = ('-requiresResponse','date_requested')  
    #List
    list_display = ('email', 'first_name', 'last_name', 
                    'date_requested', 'requiresResponse',)    
    list_filter = (ClosedQuoteFilter,)
    #Change form
    fields = ("date_requested", "first_name", "last_name", "email", "phone", 
              "cost", "comments","requiresResponse", "closed")
    readonly_fields = ('first_name', 'last_name', 'email','phone', 'date_requested')        
    search_fields = ('last_name','email')

admin.site.register(Quote, QuoteAdmin)
admin.site.add_action(CloseQuote)
admin.site.add_action(Export_Selected)