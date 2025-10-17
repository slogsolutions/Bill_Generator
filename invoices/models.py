from django.db import models
from django.utils import timezone
from datetime import datetime

class Signature(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='signatures/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Stamp(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='stamps/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    # Header Section
    invoice_number = models.CharField(max_length=50, unique=True, editable=False)
    invoice_date = models.DateField(default=timezone.now)
    sac_code = models.CharField(max_length=10, default='999293')
    
    # Client Details
    client_name = models.TextField(default='TO: THE COMMANDING OFFICER,')
    client_address = models.TextField(default='21 CGSR (A), BAIRAGARH, BHOPAL, MADHYA PRADESH-462031, INDIA')
    
    # Service Description
    contract_no = models.CharField(max_length=100, blank=True, null=True)
    contract_date = models.DateField(blank=True, null=True)
    service_description = models.TextField(
        default="""Mode of training: offline
Training frequency: Weekdays
Duration of training per day (in hours): 4
Training premise: Buyers location
Type of training: Classroom based Instructor Led Training
Course level: Intermediate
Category of training course: IT and Software
Sub-categories of training course: Network and Security
Certification: Yes
Certification programme: Participation Certificate
Type of training partner: Training institute"""
    )
    
    # Amount Section - USER ENTERS TOTAL, WE CALCULATE BASE
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # GST Section
    state = models.CharField(max_length=100, default='Uttarakhand')
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=9.00)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=9.00)
    igst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    
    # Calculated fields
    base_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    cgst_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    igst_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    round_off = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    
    # Signature
    signature = models.ForeignKey(Signature, on_delete=models.SET_NULL, null=True, blank=True)

    # Stamp related fields (correctly placed inside Invoice)
    include_stamp = models.BooleanField(default=False)
    stamp = models.ForeignKey(Stamp, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        
        # Calculate base amount from total (reverse calculation)
        # Total = Base + GST, so Base = Total / (1 + GST_Rate)
        if self.state and self.state.lower() == 'uttarakhand':
            # Total GST rate = CGST + SGST
            total_gst_rate = (self.cgst_rate or 0) + (self.sgst_rate or 0)
            self.base_amount = self.total_amount / (1 + (total_gst_rate / 100))
            self.cgst_amount = (self.base_amount * (self.cgst_rate or 0)) / 100
            self.sgst_amount = (self.base_amount * (self.sgst_rate or 0)) / 100
            self.igst_amount = 0
        else:
            # IGST for other states
            self.base_amount = self.total_amount / (1 + ((self.igst_rate or 0) / 100))
            self.cgst_amount = 0
            self.sgst_amount = 0
            self.igst_amount = (self.base_amount * (self.igst_rate or 0)) / 100
        
        # Round off calculation
        subtotal = (self.base_amount or 0) + (self.cgst_amount or 0) + (self.sgst_amount or 0) + (self.igst_amount or 0)
        rounded_total = round(subtotal)
        self.round_off = rounded_total - subtotal
        self.total_amount = rounded_total
        
        super().save(*args, **kwargs)
    
    def generate_invoice_number(self):
        today = timezone.now().date()
        
        if today.month >= 4:
            financial_year = today.year
        else:
            financial_year = today.year - 1
        
        financial_year_start = datetime(financial_year, 4, 1).date()
        financial_year_end = datetime(financial_year + 1, 3, 31).date()
        
        count = Invoice.objects.filter(
            invoice_date__gte=financial_year_start,
            invoice_date__lte=financial_year_end
        ).count() + 1
        
        return f"SLG-{financial_year}-{count:02d}"
    
    def __str__(self):
        return self.invoice_number
