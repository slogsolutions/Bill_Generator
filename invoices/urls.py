from django.urls import path
from . import views

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/pdf/', views.download_invoice_pdf, name='download_invoice_pdf'),

    path('create/', views.create_invoice, name='create_invoice'),
    path('preview/<int:pk>/', views.invoice_preview, name='invoice_preview'),
]
