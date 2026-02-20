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

from django.db.models import Avg

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

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def average_rating(self):
        """Return float average rating (1-5) or 0 if no reviews."""
        agg = self.reviews.aggregate(avg=Avg('rating'))
        return round(agg['avg'] or 0, 1)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.phone}"


class Review(models.Model):
    """Product review/rating submitted by a customer."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100, blank=True, help_text="Optional visitor name")
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating} stars for {self.product.name}"

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

class Invoice(models.Model):

    STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("partial", "Partially Paid"),
        ("paid", "Paid"),
        ("overdue", "Overdue"),
    ]

    order = models.OneToOneField(
        "Order",
        on_delete=models.CASCADE,
        related_name="invoice"
    )

    invoice_number = models.CharField(max_length=100, unique=True)

    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    gst_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="unpaid"
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.invoice_number}"


class Customer(models.Model):
    """Optional lightweight customer model for CRM linking."""
    name = models.CharField(max_length=150)
    company = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company})" if self.company else self.name


class Supplier(models.Model):
    """Supplier/vendor record for inventory sourcing."""
    name = models.CharField(max_length=150)
    contact_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StockHistory(models.Model):
    """Lightweight stock history to track changes against products."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_histories')
    change = models.IntegerField(help_text='Positive to add stock, negative to remove')
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name}: {self.change} ({self.created_at.strftime('%Y-%m-%d')})"
