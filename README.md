🏗️ Pashupatinath Marketing – B2B Construction Material Management System

A complete Django-based B2B construction material management platform designed for wholesale suppliers.
The system handles product catalog management, bulk enquiries, quotations, orders, invoices, admin analytics, and PDF quotation generation.

🚀 Project Overview

Pashupatinath Marketing is a wholesale construction materials supplier platform that allows:
Contractors & builders to browse products
Submit bulk enquiries
Receive quotations
Admins to manage enquiries via CRM-style dashboard
Generate PDF quotations
Manage Orders & Invoices
Export enquiries to Excel
This system is optimized for B2B workflow and bulk material sourcing.

🛠️ Tech Stack

Backend: Django (Python)

Frontend: HTML5, CSS3, Bootstrap 5

Database: SQLite (default) / PostgreSQL compatible

Email System: Django EmailMultiAlternatives (HTML + Text emails)

PDF Generation: ReportLab

Excel Export: OpenPyXL

Admin Dashboard: Django Admin (customized)

📂 Core Features
🏠 Public Website
1️⃣ Home Page

Hero section

Inventory navigation

Material categories

Business metrics

CTA for enquiries

2️⃣ Product Catalog

Category filtering

Product detail page

Bulk-only pricing model

3️⃣ Product Enquiry System

Linked to specific product

Stores:

Name

Phone

Email

Quantity

Message

Sends:

Email to admin

Confirmation email to customer

Tracks enquiry source

4️⃣ Contact Page

Direct enquiry form

Stored in database

Sends email notifications

📊 CRM & Admin Features
🔐 Admin Dashboard

Custom staff-only dashboard with:

Total Enquiries

Awaiting Reply

Converted Leads

Conversion Rate

Response Rate

Follow-ups Due

Revenue from Converted Leads

Last 7 Days Trend Graph

Source Analytics

Status Analytics

📌 Enquiry Management (CRM System)

Each enquiry includes:

Product (optional)

Source (Contact / Product / WhatsApp / Manual)

Status tracking:

New

Contacted

Quoted

Negotiation

Converted

Closed

Lost

Priority level (Low / Medium / High)

Assigned Sales Person

Estimated Value

Follow-up Date

Notes

Admin Actions

Export selected enquiries to Excel

Status & priority badges

Date hierarchy filtering

💰 Quotation System

One-to-one with enquiry

Includes:

Base price

GST %

Valid until date

Automatic GST calculation

Total amount calculation

📄 PDF Generation

Downloadable quotation PDF

Generated using ReportLab

Auto-updates enquiry status to "Quoted"

📦 Order Management

Orders linked to enquiries.

Statuses:

Pending

Confirmed

Shipped

Delivered

🧾 Invoice Management

Invoices linked one-to-one with Orders.

Includes:

Invoice number

Issue & due dates

GST breakdown

Payment status:

Unpaid

Partial

Paid

Overdue

🗂️ Database Models

Category

Product

Contact

Enquiry

Quotation

Order

Invoice

⚙️ Installation Guide
1️⃣ Clone Repository
git clone https://github.com/yourusername/pashupatinath-marketing.git
cd pashupatinath-marketing

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt


If not created yet, install manually:

pip install django reportlab openpyxl pillow

4️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Create Superuser
python manage.py createsuperuser

6️⃣ Run Development Server
python manage.py runserver


Visit:

http://127.0.0.1:8000/


Admin panel:

http://127.0.0.1:8000/admin/

📧 Email Configuration

Add in settings.py:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = 'admin@example.com'

📁 Project Structure (Simplified)
shop/
 ├── models.py
 ├── views.py
 ├── admin.py
 ├── templates/
 │    ├── shop/
 │    ├── admin/
 │    ├── emails/
 ├── static/

🔒 Security Notes

CSRF protection enabled

Staff-only admin dashboard

Email reply-to support

Enquiry validation checks

GST & total calculation handled server-side

📈 Future Improvements

Payment Gateway Integration

WhatsApp API automation

Sales team role permissions

REST API (Django REST Framework)

Real-time dashboard with Charts.js

Multi-branch support

Inventory stock tracking

🏢 Business Use Case

This system is ideal for:

Cement & TMT distributors

Construction wholesalers

B2B material suppliers

Industrial supply businesses

👨‍💻 Developed For

Pashupatinath Marketing
Wholesale Construction Material Supplier
Amravati, Maharashtra

📜 License

This project is proprietary software developed for internal business use.