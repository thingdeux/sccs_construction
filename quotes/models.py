from django.db import models
from datetime import datetime

# Create your models here.
class Quote(models.Model):
    email = models.EmailField("E-Mail", max_length=254, db_index=True)
    first_name = models.CharField("First Name", max_length=254, default="")
    last_name = models.CharField("Last Name", max_length=254, default="", db_index=True)
    #full_name = self.getFullName()
    phone = models.CharField("Phone", max_length=30, null=True)
    date_requested = models.DateTimeField("Quote Requested", default=datetime.now())
    comments = models.CharField("Comments", max_length=512, default="")
    requiresResponse = models.BooleanField("Response Required?", default=True)
    

    #def getFullName(self):
        #return str(self.first_name + self.last_name)

    def __unicode__(self):
        return self.email