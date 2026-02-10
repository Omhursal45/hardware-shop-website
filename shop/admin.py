from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from datetime import timedelta
from django.utils.timezone import now
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
    
    


admin.site.site_header = "Pashupathinath Marketing Admin"
admin.site.site_title = "PM Admin"
admin.site.index_title = "Dashboard"

def admin_dashboard(request):
    today = now().date()

    context = dict(
        admin.site.each_context(request),

        # cards
        total_enquiries=Enquiry.objects.count(),
        today_enquiries=Enquiry.objects.filter(created_at__date=today).count(),
        total_products=Product.objects.count(),
        total_categories=Category.objects.count(),
        total_contacts=Contact.objects.count(),

        # table
        recent_enquiries=Enquiry.objects.order_by("-created_at")[:10],
    )

    return TemplateResponse(request, "admin/dashboard.html", context)


# ---- URL wiring (correct & safe) ----
original_get_urls = admin.site.get_urls

def custom_get_urls():
    urls = original_get_urls()
    custom_urls = [
        path(
            "dashboard/",
            admin.site.admin_view(admin_dashboard),
            name="admin_dashboard"
        ),
    ]
    return custom_urls + urls

admin.site.get_urls = custom_get_urls