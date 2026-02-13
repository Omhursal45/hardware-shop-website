from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from decimal import Decimal
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.phone}"

class Enquiry(models.Model):

    SOURCE_CHOICES = [
        ("contact", "Contact Page"),
        ("product", "Product Enquiry"),
        ("whatsapp", "WhatsApp"),
        ("manual", "Manual Entry"),
    ]

    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("quoted", "Quoted"),
        ("negotiation", "Negotiation"),
        ("converted", "Converted"),
        ("closed", "Closed"),
        ("lost", "Lost"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Customer Info
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    # Enquiry Info
    quantity = models.CharField(max_length=50, blank=True)
    message = models.TextField(blank=True)

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default="contact"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    estimated_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    assigned_to = models.CharField(
        max_length=100,
        blank=True,
        help_text="Sales person name"
    )

    follow_up_date = models.DateField(null=True, blank=True)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def is_followup_due(self):
        return self.follow_up_date and self.follow_up_date <= timezone.now().date()

    def __str__(self):
        return f"{self.name} - {self.phone}"

class Quotation(models.Model):
    enquiry = models.OneToOneField(
        Enquiry,
        on_delete=models.CASCADE,
        related_name="quotation"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=18)
    valid_until = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def gst_amount(self):
        return (self.price * self.gst_percentage) / Decimal("100")
    
    def total_amount(self):
        return self.price + self.gst_amount()
    
    def __str__(self):
        return f"Quatition for {self.enquiry.name}"
    

class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
    ]

    customer = models.CharField(max_length=150)
    enquiry = models.ForeignKey("Enquiry", on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"
