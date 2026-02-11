from django.shortcuts import render,redirect
from .models import Category,Product,Enquiry
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Contact
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from django.db.models import Count,Sum
from django.db.models.functions import TruncDate

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table,TableStyle
from reportlab.lib.units import inch
from .models import Quotation
from django.http import HttpResponse

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

# def contact(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         message = request.POST.get('message')
        
#         messages.success(request, 'Thank you! Our team will contact you within 24 hours.')
#         return redirect('contact')
#     return render(request, 'shop/contact.html')

def enquiry(request):
    product = None

    product_id = request.GET.get("product")
    if product_id:
        product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        print("🔥 PRODUCT ENQUIRY HIT 🔥")
        print("POST DATA:", request.POST)

        product_id = request.POST.get("product_id")
        if not product_id:
            messages.error(request, "Invalid product.")
            return redirect(request.path)

        product = get_object_or_404(Product, id=product_id)

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email", "").strip()
        quantity = request.POST.get("quantity")
        message = request.POST.get("message", "")

        if not all([name, phone, quantity]):
            messages.error(request, "Please fill all required fields.")
            return redirect(request.path)

        enquiry_obj = Enquiry.objects.create(
            product=product,
            name=name,
            phone=phone,
            email=email,
            quantity=quantity,
            message=message,
            source="product",  
        )

        print("✅ ENQUIRY SAVED:", enquiry_obj.id)

        try:
            admin_subject = f"New Product Enquiry – {product.name}"

            admin_html = render_to_string(
                "emails/admin_enquiry.html",
                {
                    "product": product,
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "quantity": quantity,
                    "message": message,
                }
            )

            admin_text = f"""
New Product Enquiry

Product: {product.name}
Name: {name}
Phone: {phone}
Email: {email or 'N/A'}
Quantity: {quantity}

Message:
{message}
            """

            email_admin = EmailMultiAlternatives(
                subject=admin_subject,
                body=admin_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
                reply_to=[email] if email else None,
            )
            email_admin.attach_alternative(admin_html, "text/html")
            email_admin.send(fail_silently=True)

            print("✅ ADMIN EMAIL SENT")

        except Exception as e:
            print("❌ ADMIN EMAIL ERROR:", e)

        if email:
            try:
                customer_subject = "We Received Your Product Enquiry"

                customer_html = render_to_string(
                    "emails/customer_enquiry.html",
                    {
                        "name": name,
                        "product": product,
                    }
                )

                customer_text = f"""
Dear {name},

Thank you for enquiring about {product.name}.
Our team will contact you within 24 hours.

Regards,
Pashupatinath Marketing
                """

                email_customer = EmailMultiAlternatives(
                    subject=customer_subject,
                    body=customer_text,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
                email_customer.attach_alternative(customer_html, "text/html")
                email_customer.send(fail_silently=True)

                print("✅ CUSTOMER EMAIL SENT")

            except Exception as e:
                print("❌ CUSTOMER EMAIL ERROR:", e)

        messages.success(
            request,
            "Your product enquiry has been submitted successfully."
        )

        return redirect("enquiry_success")

    return render(request, "shop/enquiry.html", {
        "product": product
    })



def contact(request):
    if request.method == "POST":
        print("🔥 CONTACT FORM HIT 🔥")
        print("POST DATA:", request.POST)

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if not all([name, phone, email, message]):
            messages.error(request, "All fields are required.")
            return redirect("contact")

        Enquiry.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message,
            source = "contact",
        )
        
        try:
            admin_subject = "New Contact Enquiry - Pashupatinath Marketing"

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
New Contact Enquiry

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
            email_admin.send()

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
            )
            email_customer.attach_alternative(customer_html, "text/html")
            email_customer.send()

            print("✅ CUSTOMER EMAIL SENT")

        except Exception as e:
            print("❌ CUSTOMER EMAIL FAILED:", e)

        messages.success(
            request,
            "Your enquiry has been received. Our team will contact you shortly."
        )
        return redirect("contact")

    return render(request, "shop/contact.html")



@staff_member_required
def admin_dashboard(request):

    today = now().date()
    last_7_days = today - timedelta(days=7)

    enquiries = Enquiry.objects.all()
    
    total_enquiries = enquiries.count()

    awaiting_reply = enquiries.filter(status="new").count()

    responded_count = enquiries.exclude(status="new").count()

    conversions = enquiries.filter(status="converted").count()

    followups_due = enquiries.filter(
        follow_up_date__lte=today
    ).exclude(status="converted").count()

    response_rate = round(
        (responded_count / total_enquiries) * 100
    ) if total_enquiries > 0 else 0

    conversion_rate = round(
        (conversions / total_enquiries) * 100
    ) if total_enquiries > 0 else 0
    
    trend_data = (
        enquiries
        .filter(created_at__date__gte=last_7_days)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    )

    trend_labels = [str(d["day"]) for d in trend_data]
    trend_values = [d["total"] for d in trend_data]

    source_data = enquiries.values("source").annotate(total=Count("id"))

    source_labels = [
        dict(Enquiry.SOURCE_CHOICES).get(s["source"], "Unknown")
        for s in source_data
    ]

    source_values = [s["total"] for s in source_data]

    status_data = enquiries.values("status").annotate(total=Count("id"))

    status_labels = [
        dict(Enquiry.STATUS_CHOICES).get(s["status"], "Unknown")
        for s in status_data
    ]

    status_values = [s["total"] for s in status_data]

    total_revenue = enquiries.filter(
        status="converted"
    ).aggregate(
        total=Sum("estimated_value")
    )["total"] or 0

    recent_enquiries = (
        enquiries
        .select_related("product")
        .order_by("-created_at")[:10]
    )

    context = {
        "total_enquiries": total_enquiries,
        "awaiting_reply": awaiting_reply,
        "responded_count": responded_count,
        "conversions": conversions,
        "response_rate": response_rate,
        "conversion_rate": conversion_rate,
        "followups_due": followups_due,
        "total_revenue": total_revenue,
        "trend_labels": trend_labels,
        "trend_values": trend_values,
        "source_labels": source_labels,
        "source_values": source_values,
        "status_labels": status_labels,
        "status_values": status_values,
        "recent_enquiries": recent_enquiries,
    }

    return render(request, "admin/dashboard.html", context)

def enquiry_success(request):
    return render(request, "shop/enquiry_success.html")


def generate_quotation_pdf(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    enquiry = quotation.enquiry
    
    response = HttpResponse(content_type ="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=quotation_{quotation.id}.pdf"
    
    doc = SimpleDocTemplate(response)
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph("<b>Pashupathinath Marketing</b>", styles['Title']))
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph(f"Customer : {enquiry.name}", styles["Normal"]))
    elements.append(Paragraph(f"Phone : {enquiry.phone}", styles["Normal"]))
    elements.append(Paragraph(f"Email : {enquiry.email}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    data = [
        ["Product", enquiry.product.name if enquiry.product else "-"],
        ["Quantity", enquiry.quantity],
        ["Base Price", f"₹ {quotation.price}"],
        ["GST", f"{quotation.gst_percentage}%"],
        ["Total Amount", f"₹ {quotation.total_amount()}"],
        ["Valid Until", quotation.valid_until.strftime("%d-%m-%Y")],
    ]
    
    table = Table(data, colWidths=[2*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    
    elements.append(table)
    
    doc.build(elements)
    
    enquiry.status = "quoted"
    enquiry.save()
    
    return response
    