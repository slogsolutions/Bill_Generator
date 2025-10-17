from django.contrib import admin
from .models import Invoice, Signature

@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'invoice_date', 'total_amount', 'state', 'created_at']
    list_filter = ['invoice_date', 'state']
    search_fields = ['invoice_number', 'client_name']
    readonly_fields = ['invoice_number', 'cgst_amount', 'sgst_amount', 'igst_amount', 'round_off', 'total_amount']
