from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Invoice, Signature
from .forms import InvoiceForm
from num2words import num2words
from django.contrib.auth.decorators import login_required, permission_required
# ReportLab imports (kept in case you still use other reportlab views)
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import redirect
# xhtml2pdf imports (new)
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa
import os

# ======== Simple Hardcoded Login ========
def require_login_session(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get("is_authenticated"):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped

def login_view(request):
    # Hardcoded credentials
    HARDCODED_USERNAME = "surajslog"
    HARDCODED_PASSWORD = "kiranslog"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == HARDCODED_USERNAME and password == HARDCODED_PASSWORD:
            
            request.session["is_authenticated"] = True
            request.session.cycle_key()
            return redirect("invoice_list")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "invoices/login.html")


def logout_view(request):
    request.session.flush()
    return redirect("login")

@require_login_session
@require_POST

def invoice_delete(request, pk):
    """
    Delete an invoice. Only accepts POST (safe).
    Redirects back to invoice list after deletion.
    """
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    # optional: you can add messages framework to show a success toast
    return redirect(reverse('invoice_list'))

@require_login_session
def create_invoice(request):
    if not request.session.get("is_authenticated"):
        return redirect('login')
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            return redirect('invoice_preview', pk=invoice.pk)
    else:
        form = InvoiceForm()
    
    return render(request, 'invoices/create_invoice.html', {'form': form})

@require_login_session
def invoice_preview(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    # Convert amount to words
    amount_in_words = num2words(int(invoice.total_amount), lang='en_IN').title()
    
    context = {
        'invoice': invoice,
        'amount_in_words': amount_in_words,
    }
    
    return render(request, 'invoices/invoice_preview.html', context)

@require_login_session
def invoice_list(request):
    # if not logged in via our simple session flag, send to login page
    if not request.session.get("is_authenticated"):
        return redirect('login')

    invoices = Invoice.objects.all()
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})



# Helper for xhtml2pdf to find static and media files
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access static/media files.
    """
    # If uri is a media url, map to MEDIA_ROOT
    if uri.startswith(settings.MEDIA_URL):
        path = uri.replace(settings.MEDIA_URL, '')
        return os.path.join(settings.MEDIA_ROOT, path)

    # If uri is a static url, map to STATIC_ROOT if available, otherwise to project static folder
    if uri.startswith(settings.STATIC_URL):
        path = uri.replace(settings.STATIC_URL, '')
        if getattr(settings, 'STATIC_ROOT', None):
            return os.path.join(settings.STATIC_ROOT, path)
        # fallback to static folder in BASE_DIR
        return os.path.join(settings.BASE_DIR, 'static', path)

    # return unchanged for absolute paths or external URLs
    return uri

@require_login_session
def download_invoice_pdf(request, pk):
    """
    Generates a PDF using xhtml2pdf (pisa) from the same template used for preview.
    This inlines the contents of static/css/styles.css so the PDF matches the browser preview.
    """
    invoice = get_object_or_404(Invoice, pk=pk)

    # Build context same as preview
    amount_in_words = num2words(int(invoice.total_amount), lang='en_IN').title()
    context = {
        'invoice': invoice,
        'amount_in_words': amount_in_words,
    }

    # Load the HTML template (same template used for preview)
    template = get_template('invoices/invoice_preview.html')
    html = template.render(context)

    # Read the CSS file from static and inline it (xhtml2pdf cannot reliably fetch CSS over HTTP)
    css_path = os.path.join(settings.BASE_DIR, 'static', 'css', 'styles.css')
    css_text = ''
    if os.path.exists(css_path):
        try:
            with open(css_path, 'r', encoding='utf-8') as f:
                css_text = f.read()
        except Exception:
            css_text = ''

    # Prepend the CSS to the rendered HTML
    html_with_css = '<style>%s</style>\n%s' % (css_text, html)

    # Create PDF
    result = io.BytesIO()
    pdf_status = pisa.CreatePDF(
        src=io.BytesIO(html_with_css.encode('utf-8')),
        dest=result,
        link_callback=link_callback
    )

    if pdf_status.err:
        # Return a readable error (useful while developing)
        return HttpResponse('We had errors while generating the PDF: <pre>%s</pre>' % pdf_status.err, status=500)

    result.seek(0)
    return HttpResponse(result.getvalue(), content_type='application/pdf')
