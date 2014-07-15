from django.contrib import admin
from quotes.models import Quote

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

# Register your models here.
class QuoteAdmin(admin.ModelAdmin):
    fields = ("date_requested", "first_name", "last_name", "email", "phone", 
              "requiresResponse", "closed", "cost", "comments",)
    #readonly_fields = ('email','phone')
    readonly_fields = ('date_requested', )
    list_display = ('email', 'first_name', 'last_name', 
                    'date_requested', 'requiresResponse',)    
    search_fields = ('last_name','email')    
    list_filter = (ClosedQuoteFilter,)    
    
admin.site.register(Quote, QuoteAdmin)