from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from quotes.models import Quote, QuoteSubmissionForm, sendMailToContacts
from django.utils.timezone import now
from quotes.log import log
from datetime import datetime
from django.views.decorators.cache import cache_page


# Basic Direct to Template Views.
# 86400 Seconds == 24 Hours - This cached page will expire once every 30 days
@cache_page(86400 * 30)
def Index(request):
    current_year = now().year
    return render(request, 'quotes/index.html', {"current_year": current_year})
# 86400 Seconds == 24 Hours - This cached page will expire once every 30 days
@cache_page(86400 * 30)
def Services(request):
    current_year = now().year
    return render(request, 'quotes/services.html', {"current_year": current_year})
# 86400 Seconds == 24 Hours - This cached page will expire once every 30 days
@cache_page(86400 * 30)
def AboutUs(request):
    current_year = now().year
    return render(request, 'quotes/aboutus.html', {"current_year": current_year})


# Dynamic URL end points
@cache_page(86400 * 30)
def Thanks(request):
    current_year = now().year
    # Passes the first name from the contact form and thanks the submitter
    try:
        first_name = request.GET['r'][:254]
        template_name = 'quotes/thanks.html'
        return render(request, template_name, {'name': first_name, "current_year": current_year})
    except:
        # If no name is passed return 404
        raise Http404


def SubmitQuote(request):
    current_year = now().year
    if request.method == 'POST':
        # Create form instance and pull in data from the front-end
        form = QuoteSubmissionForm(request.POST)

        # Make sure submitted info is valid
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            comments = form.cleaned_data['comments']

            try:
                # Try to save DB Record
                new_record = Quote(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    comments=comments,
                    date_requested=now(),
                    requiresResponse=False,
                    closed=False,
                    cost=0
                )
                # Save new quote record entry
                new_record.save()

                # Build E-Mail Templates
                generated_html = render_to_string('quotes/email_html.html',
                                                  {'quote': new_record})
                generated_txt = render_to_string('quotes/email_text.html',
                                                 {'quote': new_record})

                # Get first name to pass to /thanks
                first_name = str(new_record.first_name)
                sendMailToContacts(first_name, generated_html, generated_txt)

            except Exception as err:
                log(err)

            return HttpResponseRedirect('/thanks/?r=' + str(first_name))
    else:
        form = QuoteSubmissionForm()

    template_name = 'quotes/submitQuote.html'
    return render(request, template_name, {'form': form, 'current_year': current_year})


def Export(request):
    # Get current time for report generated on date/time
    now = datetime.now()

    try:
        # Get list of selected quotes
        ids = request.GET['ids']
        # Build two variables - one a list for the quote query,
        # the other a string to pass to the ExportToXLS
        # link should it be clicked.
        built_query = []
        export_query = "?exp="

        for quote_id in ids.split(','):
            built_query.append(str(quote_id))
            if export_query is "?exp=":
                export_query = export_query + str(quote_id)
            else:
                export_query = export_query + "," + str(quote_id)

        # DB Query for results
        results = Quote.objects.filter(pk__in=built_query)
        # Render Template
        template_name = 'quotes/export.html'
    except Exception as err:
        log(err)

    return render(request, template_name, {'report_results': results,
                  'datetime': now, 'exportQuery': export_query})


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

    if request.GET['exp'] == u'All':
        query = Quote.objects.all()
    else:
        for quote_id in request.GET['exp'].split(','):
            built_query.append(str(quote_id))

        query = Quote.objects.filter(pk__in=built_query)

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    # For iteration of spreadsheet columns
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
        ws.write(0, col_num, column_name, font_style)
        ws.col(col_num).width = column_length
        col_num += 1

    # For iteration of spreadsheet rows
    row_num = 1
    for quote in query:
        # Write each of the values from the query to the spreadsheet
        ws.write(row_num, 0, quote.first_name)
        ws.write(row_num, 1, quote.last_name)
        ws.write(row_num, 2, quote.email)
        ws.write(row_num, 3, quote.phone)
        ws.write(row_num, 4, str(quote.date_requested.strftime("%m/%d/%y")))
        ws.write(row_num, 5, quote.comments)
        ws.write(row_num, 6, boolToYesNo(quote.requiresResponse))
        ws.write(row_num, 7, boolToYesNo(quote.closed))
        ws.write(row_num, 8, quote.cost)
        ws.write(row_num, 9, str(quote.id))
        row_num += 1

    wb.save(response)

    return response
