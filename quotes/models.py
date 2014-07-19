from django.db import models
from datetime import datetime
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.core import mail
from django.core.mail import EmailMultiAlternatives

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

#HTML form for submission of quotes
class QuoteSubmissionForm(ModelForm):    
    class Meta:
        model = Quote            
        fields = ['first_name', 'last_name', 'email', 'phone', 'comments']

#E-Mails that should receive notifications of new quotes
class ContactEmail(models.Model):
    name = models.CharField("Name", max_length=254)
    email = models.EmailField("E-Mail Address", max_length=254, db_index=True)

    def __unicode__(self):
        return self.email


def sendMailToContacts(name, html, text):    
    #Get a list of all of the current contactees
    contacts = ContactEmail.objects.all()    
    email_addresses = []
    #Build E-Mail
    subject = str(name) + " has requested a Quote on SCCS"
    text_message = text
    html_message = html
    from_addr = "uberbreaker@gmail.com"

    #Create List of e-mail addresses
    for address in contacts:
        email_addresses.append(address.email)


    try:
        #Get django e-mail settings        
        connection = mail.get_connection()        
        #Open E-Mail server connection        
        connection.open()        
        #Append RAW Text
        email_message = EmailMultiAlternatives(subject, text_message, from_addr, email_addresses, connection=connection)
        #Append HTML
        email_message.attach_alternative(html_message, "text/html")
        #Send Message
        email_message.send()    

        connection.close()
    except Exception as err:
        connection.close()
        print err