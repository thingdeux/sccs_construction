from django.contrib import admin
from quotes.models import Quote

# Register your models here.
class QuoteAdmin(admin.ModelAdmin):
    fields = ("first_name", "last_name", ("email", "phone"),"date_requested", "requiresResponse", "comments")
    #readonly_fields = ('email','phone')
    #readonly_fields = ('date_requested')

    list_display = ('email', 'first_name', 'last_name', 
                    'date_requested', 'requiresResponse')
    search_fields = ('last_name',)    

admin.site.register(Quote, QuoteAdmin)