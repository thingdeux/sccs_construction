from django.db import models
from datetime import datetime
from django.forms import ModelForm
from django.core.exceptions import ValidationError

# Create your models here.
class Quote(models.Model):    
    email = models.EmailField("E-Mail", max_length=254, db_index=True)
    first_name = models.CharField("First Name", max_length=254, default="")
    last_name = models.CharField("Last Name", max_length=254, default="", db_index=True)    
    phone = models.CharField("Phone", max_length=30, null=True, blank=True) #Not Required
    date_requested = models.DateTimeField("Date Quote Requested", default=datetime.now())    
    comments = models.TextField("Comments", max_length=512)
    requiresResponse = models.BooleanField("Responded To?", default=False)
    closed = models.BooleanField("Quote Closed", default=False)
    cost = models.DecimalField(max_digits=12, decimal_places=2, db_index=True, default=0.00)

    def __unicode__(self):
        return self.email

class QuoteSubmissionForm(ModelForm):
    class Meta:
        model = Quote
        fields = ['first_name', 'last_name', 'email', 'phone', 'comments']
