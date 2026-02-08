from django.shortcuts import render,redirect
from .models import Category , Product ,Enquiry
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
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

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')

        enquiry = Enquiry.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message
        )

        send_mail(
            subject="New Contact Enquiry - Pashupatinath Marketing",
            message=f"""
New enquiry received:

Name: {name}
Phone: {phone}
Email: {email}

Message:
{message}
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        send_mail(
            subject="Welcome to Pashupatinath Marketing",
            message=f"""
Dear {name},

Thank you for contacting Pashupatinath Marketing.

We have received your enquiry and our team will get back to you within 24 hours.

📍 Address:
Pashupatinath Marketing, Main Road,
Amravati, Maharashtra - 444601

📞 Phone:
+91 98765 43210

📧 Email:
support@pashupatinath.com

Best Regards,
Pashupatinath Marketing Team
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        messages.success(request, "Your enquiry has been submitted successfully.")
        return redirect('contact')

    return render(request, 'contact.html')
