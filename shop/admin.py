from django.contrib import admin
from .models import Category, Product, Enquiry


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'phone', 'quantity', 'created_at')
    search_fields = ('name', 'phone', 'product__name')
    list_filter = ('created_at',)
