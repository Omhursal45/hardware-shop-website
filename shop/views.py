from django.shortcuts import render,redirect
from .models import Category , Product ,Enquiry
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def home(request):
    return render(request, 'shop/home.html')

def product_detail(request, slug):
    product = Product.objects.get(slug=slug, is_available=True)
    return render(request, 'shop/product_details.html', {
        'product' : product
    })

def products(request):
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_available=True)

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'shop/products.html', {
        'categories': categories,
        'products': products
    })


def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        messages.success(request, 'Thank you! Our team will contact you within 24 hours.')
        return redirect('contact')
    return render(request, 'shop/contact.html')




def enquiry(request):
    product = None

    product_id = request.GET.get('product')
    if product_id:
        product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        Enquiry.objects.create(
            product=product,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            quantity=request.POST.get('quantity'),
            message=request.POST.get('message'),
        )

        return render(request, 'shop/enquiry_success.html', {
            'product': product
        })

    return render(request, 'shop/enquiry.html', {
        'product': product
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Enquiry


def contact_view(request):
    if request.method == "POST":
        print("🔥 CONTACT FORM HIT 🔥")
        print("POST DATA:", request.POST)

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Basic validation
        if not all([name, phone, email, message]):
            messages.error(request, "All fields are required.")
            return redirect("contact")
        Enquiry.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message
        )
        try:
            admin_subject = "New Bulk Enquiry - Pashupatinath Marketing"

            admin_html = render_to_string(
                "emails/admin_enquiry.html",
                {
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "message": message,
                }
            )

            admin_text = f"""
New Enquiry Received

Name: {name}
Phone: {phone}
Email: {email}

Message:
{message}
            """

            email_admin = EmailMultiAlternatives(
                subject=admin_subject,
                body=admin_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
                reply_to=[email],
            )

            email_admin.attach_alternative(admin_html, "text/html")
            email_admin.send(fail_silently=False)
            print("✅ ADMIN EMAIL SENT")

        except Exception as e:
            print("❌ ADMIN EMAIL FAILED:", e)

        try:
            customer_subject = "We Received Your Enquiry | Pashupatinath Marketing"

            customer_html = render_to_string(
                "emails/customer_welcome.html",
                {"name": name}
            )

            customer_text = f"""
Dear {name},

Thank you for contacting Pashupatinath Marketing.
Our team will contact you within 24 hours.

Regards,
Pashupatinath Marketing
            """

            email_customer = EmailMultiAlternatives(
                subject=customer_subject,
                body=customer_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
                reply_to=[settings.ADMIN_EMAIL],
            )

            email_customer.attach_alternative(customer_html, "text/html")
            email_customer.send(fail_silently=False)
            print("✅ CUSTOMER EMAIL SENT")

        except Exception as e:
            print("❌ CUSTOMER EMAIL FAILED:", e)

        messages.success(
            request,
            "Your enquiry has been received. Our team will contact you shortly."
        )

        return redirect("contact")

    return render(request, "contact.html")
