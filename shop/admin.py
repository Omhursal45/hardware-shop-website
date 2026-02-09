from django.contrib import admin
from .models import Category, Product, Enquiry, Contact


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
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_change_permission(self ,request, obj=None):
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        return False

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone" , "email", "created_at")
    search_fields = ("name","phone","email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    