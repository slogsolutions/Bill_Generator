from django import forms
from .models import Invoice, Signature

INDIAN_STATES = [
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttarakhand', 'Uttarakhand'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('West Bengal', 'West Bengal'),
    ('Delhi', 'Delhi'),
]

class InvoiceForm(forms.ModelForm):
    state = forms.ChoiceField(choices=INDIAN_STATES, initial='Uttarakhand')
    
    class Meta:
        model = Invoice
        fields = [
            'sac_code', 'client_name', 'client_address', 
            'contract_no', 'contract_date', 'service_description',
            'total_amount', 'state', 'cgst_rate', 'sgst_rate', 
            'igst_rate', 'signature', 'include_stamp', 'stamp'
        ]
        widgets = {
            'sac_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '999293'
            }),
            'client_name': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'TO: THE COMMANDING OFFICER,'
            }),
            'client_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '21 CGSR (A), BAIRAGARH, BHOPAL, MADHYA PRADESH-462031, INDIA'
            }),
            'contract_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contract No: GEMC-511687711779995 (Optional)'
            }),
            'contract_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Contract Date (Optional)'
            }),
            'service_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 12,
                'placeholder': 'Enter service description here...'
            }),
            'total_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter total amount (including GST)',
                'step': '0.01'
            }),
            'cgst_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '9.00',
                'step': '0.01'
            }),
            'sgst_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '9.00',
                'step': '0.01'
            }),
            'igst_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '18.00',
                'step': '0.01'
            }),
            'signature': forms.Select(attrs={
                'class': 'form-control'
            }),
            'include_stamp': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_include_stamp'}),
            'stamp': forms.Select(attrs={'class': 'form-control', 'id': 'id_stamp'}),
        }
        labels = {
            'total_amount': 'Total Amount (Including GST)',
        }
