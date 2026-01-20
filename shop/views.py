from django.shortcuts import render
from .models import Category , Product
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
    return render(request, 'shop/contact.html')

def enquiry(request):
    return render(request, 'shop/enquiry.html')


from django.shortcuts import render, redirect

def contact_view(request):
    if request.method == "POST":
        return render(request, 'enquiry.html') 
    return render(request, 'contact.html')