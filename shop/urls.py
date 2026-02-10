from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('enquiry/', views.enquiry, name='enquiry'),
    path('enquiry-success/', views.enquiry_success, name='enquiry_success'),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
