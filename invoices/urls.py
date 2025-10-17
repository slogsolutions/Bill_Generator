from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/pdf/', views.download_invoice_pdf, name='download_invoice_pdf'),
    path('invoice/<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),
    path('create/', views.create_invoice, name='create_invoice'),
    path('preview/<int:pk>/', views.invoice_preview, name='invoice_preview'),
]
