from django.urls import path
from . import views
from .views import generate_quotation_pdf, signup_view
from .views import signup_view, login_view, logout_view

urlpatterns = [
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('', views.home, name='home'),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('products/', views.products, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('autocomplete/', views.product_autocomplete, name='product_autocomplete'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    path('enquiry/', views.enquiry, name='enquiry'),
    path('enquiry-success/', views.enquiry_success, name='enquiry_success'),
    path('quotation/<int:quotation_id>/pdf/', generate_quotation_pdf, name="quotation_pdf")
    
]
