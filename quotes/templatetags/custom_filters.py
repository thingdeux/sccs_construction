from django import template
register = template.Library()

#For adding an attribute to a field form
@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})