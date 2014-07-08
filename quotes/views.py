from django.shortcuts import render
from quotes.models import Quote

# Create your views here.
def Index(request):
    template_name = 'quotes/index.html'

    return render(request, template_name)

def Quote(request):
    template_name = 'quotes/quote.html'

    return render(request, template_name)


'''
def Search(request):
    template_name = 'tracker/search.html'
    #Take up to 5 characters max for the query
    zip_query = request.GET.get('zip')[:5]

    #Pull a list of the current missing pets from the above zip
    missing_pets = LostPet.objects.order_by('answers_to').filter(location__zip_code=zip_query, status="MISSING")    
    found_pets = LostPet.objects.order_by('answers_to').filter(location__zip_code=zip_query, status="FOUND")[:5]

    return render(request, template_name, {'missing_pets': missing_pets, 'found_pets': found_pets, 'zip': zip_query} )
'''