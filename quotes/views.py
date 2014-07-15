from django.http import HttpResponse
from django.shortcuts import render
from quotes.models import Quote
from datetime import datetime


# Create your views here.
def Index(request):
    template_name = 'quotes/index.html'
    return render(request, template_name)

def ViewQuote(request):
    template_name = 'quotes/quote.html'
    return render(request, template_name)

def Export(request):
    #Get current time for report generated on date/time    
    now = datetime.now()
    #Get list of selected quotes
    ids = request.GET['ids']
    #Build two variables - one a list for the quote query, 
    #the other a string to pass to the ExportToXLS link should it be clicked.
    built_query = []
    export_query = "?exp="

    for quote_id in ids.split(','):
        built_query.append(str(quote_id))
        if export_query is "?exp=":
            export_query = export_query + str(quote_id)
        else:
            export_query = export_query + "," + str(quote_id)

    #DB Query for results
    results = Quote.objects.filter(pk__in=built_query)    
    #Render Template
    template_name = 'quotes/export.html'

    return render(request, template_name, {'report_results': results, 'datetime': now, 'exportQuery': export_query})

def ExportToXLS(request):
    def boolToYesNo(booleanValue):
        if booleanValue is True:
            return "Yes"
        elif booleanValue is False:
            return "No"
        else:
            return ""


    import xlwt
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=report.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Report")
    built_query = []

    for quote_id in request.GET['exp'].split(','):
        built_query.append(str(quote_id))

    query = Quote.objects.filter(pk__in=built_query)
    
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    #For iteration of columns
    col_num = 0
    columns = [
        ("First Name", 3000),
        ("Last Name", 3000),
        ("E-Mail", 4000),
        ("Phone", 3000),
        ("Requested Date", 4000),
        ("Comments", 6000),
        ("Requires Response", 5000),
        ("Closed", 2000),
        ("Cost", 2000),
        ("ID", 4000),
    ]

    for column_name, column_length in columns:
        ws.write(0,col_num, column_name, font_style)
        ws.col(col_num).width = column_length
        col_num += 1
    
    #For iteration of rows
    row_num = 1
    for quote in query:
        print quote.date_requested.strftime("%m/%d/%y")
        ws.write(row_num, 0, quote.first_name)
        ws.write(row_num, 1, quote.last_name)
        ws.write(row_num, 2, quote.email)
        ws.write(row_num, 3, quote.phone)
        ws.write(row_num, 4, str(quote.date_requested.strftime("%m/%d/%y")) )
        ws.write(row_num, 5, quote.comments)
        ws.write(row_num, 6, boolToYesNo(quote.requiresResponse) )
        ws.write(row_num, 7, boolToYesNo(quote.closed) )
        ws.write(row_num, 8, quote.cost)
        ws.write(row_num, 9, str(quote.id) )
        row_num += 1

    wb.save(response)

    return response

