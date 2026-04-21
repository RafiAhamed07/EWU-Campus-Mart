# EWU Campus Mart

A modern, full-featured e-commerce marketplace platform designed specifically for Eastern West University (EWU) students. EWU Campus Mart enables students to buy and sell products within a secure, campus-community environment with integrated payment processing and seller management.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Key Components](#key-components)
- [Contributing](#contributing)

## Features

### For Buyers
- **Secure Authentication**: Email-based login with EWU domain verification (@std.ewubd.edu or @ewubd.edu)
- **Product Browsing**: Browse products by category with detailed product information
- **Shopping Cart**: Add products to cart with variant selection (colors, sizes, options)
- **Order Management**: Place orders, track status, and view order history
- **User Profile**: Manage profile information and upload profile pictures
- **Secure Payments**: Integrated SSLCommerz payment gateway for safe transactions

### For Sellers
- **Seller Application System**: Apply to become a seller with approval workflow
- **Product Management**: Create, update, and manage product listings
- **Pricing & Offers**: Set base prices and offer prices for discounts
- **Product Variants**: Add color and size variants with individual pricing
- **Order Processing**: Accept, reject, or ship orders; track delivery status
- **Shop Banner**: Create branded shop banners for store customization
- **Sales Dashboard**: Monitor sales and order activity

### For Administrators
- **Admin Panel**: Django admin interface for content and user management
- **Seller Approval**: Manage seller requests and applications
- **Order Oversight**: Monitor all orders and transactions
- **Category Management**: Create and manage product categories
- **User Management**: Manage user accounts and permissions

## Technology Stack

- **Backend**: Django 4.2.29
- **Database**: SQLite3
- **Frontend**: 
  - Bootstrap5 (django-bootstrap-v5)
  - Tailwind CSS
  - PostCSS
- **Authentication**: Django's custom authentication with email-based login
- **Payment Gateway**: SSLCommerz
- **Image Processing**: Pillow
- **HTTP Client**: Requests
- **Environment Management**: python-dotenv

## Project Structure

```
ewustdmart/
├── buyer/                      # Buyer module
│   ├── models.py               # User models, SellerRequest
│   ├── views.py                # Buyer views and logic
│   ├── forms.py                # Login, signup forms
│   ├── urls.py                 # Buyer URL routing
│   ├── templates/              # Buyer templates
│   │   ├── buyer_home.html
│   │   ├── buyer_login.html
│   │   ├── buyer_signup.html
│   │   ├── buyer_profile.html
│   │   ├── buyer_dashboard.html
│   │   ├── buyer_profile_update.html
│   │   ├── cart.html
│   │   └── product_detail.html
│   └── static/                 # Static files
│
├── seller/                     # Seller module
│   ├── models.py               # SellerBanner model
│   ├── views.py                # Seller views and logic
│   ├── forms.py                # Seller forms
│   ├── urls.py                 # Seller URL routing
│   ├── templates/              # Seller templates
│   └── static/                 # Static files
│
├── products/                   # Product catalog module
│   ├── models.py               # Category, Product, ProductOption, Variants
│   ├── views.py                # Product views
│   ├── forms.py                # Product forms
│   ├── templates/products/     # Product templates
│   └── migrations/             # Database migrations
│
├── orders/                     # Order management module
│   ├── models.py               # Order, OrderItem models
│   ├── views.py                # Order processing views
│   ├── urls.py                 # Order URL routing
│   ├── templates/              # Order templates
│   │   ├── checkout.html
│   │   ├── order_detail.html
│   │   ├── my_orders.html
│   │   ├── success.html
│   │   ├── fail.html
│   │   └── cancel.html
│   └── migrations/             # Database migrations
│
├── home/                       # Home/public pages module
│   ├── views.py                # Home page views
│   ├── urls.py                 # Home URL routing
│   └── templates/              # Home templates
│       ├── home.html
│       ├── about.html
│       └── contact.html
│
├── base/                       # Base/shared module
│   └── models.py               # BaseModel abstract model
│
├── media/                      # User-uploaded media
│   ├── profile/                # User profile images
│   ├── product/                # Product images
│   ├── categories/             # Category images
│   └── banners/                # Seller banners
│
├── ewustdmart/                 # Main project settings
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
│
├── manage.py                   # Django management script
├── db.sqlite3                  # SQLite database
├── requirements.txt            # Python dependencies
├── package.json                # Node.js dependencies (Tailwind)
├── tailwind.config.js          # Tailwind configuration
├── postcss.config.js           # PostCSS configuration
└── README.md                   # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Node.js and npm (for Tailwind CSS)
- Git

### Clone the Repository

```bash
git clone <repository-url>
cd "EWU student Mart"
```

### Create Virtual Environment

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Windows (Command Prompt)
python -m venv .venv
.venv\Scripts\activate.bat

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Install Node Dependencies (for Tailwind CSS)

```bash
npm install
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Example .env file
DEBUG=True
SECRET_KEY=your-secret-key-here
SSLCOMMERZ_STORE_ID=your-store-id
SSLCOMMERZ_STORE_PASSWORD=your-store-password
```

### Settings Overview

Key settings in [ewustdmart/settings.py](ewustdmart/ewustdmart/settings.py):

- **EMAIL VALIDATION**: Only EWU email addresses (@std.ewubd.edu or @ewubd.edu) can register
- **DATABASE**: SQLite3 (configured as default)
- **INSTALLED APPS**: buyer, seller, home, products, orders, bootstrap5
- **MEDIA FILES**: Configured for user uploads (profile images, product images, banners)
- **STATIC FILES**: Configured for CSS, JavaScript, and images

## Database Setup

### Run Migrations

```bash
cd ewustdmart
python manage.py migrate
```

### Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
# Enter email: admin@std.ewubd.edu
# Enter password: [your-password]
```

### Load Initial Data (Optional)

```bash
python manage.py loaddata initial_data
```

## Running the Application

### Development Server

```bash
cd ewustdmart
python manage.py runserver
```

The application will be available at: `http://localhost:8000`

### Build Tailwind CSS (for development)

In a new terminal, run:

```bash
npm run dev
```

Or for production build:

```bash
npm run build
```

### Access the Admin Panel

Navigate to `http://localhost:8000/admin/` and log in with your superuser credentials.

## Usage

### User Registration

1. **Buyers**: Click "Sign Up" and enter an EWU email address
2. **Sellers**: Apply for seller status from the dashboard (admin approval required)

### For Buyers

1. Browse products by category
2. View product details with variants
3. Add items to shopping cart
4. Proceed to checkout
5. Select payment method
6. Complete payment via SSLCommerz
7. Track order status from dashboard

### For Sellers

1. Apply to become a seller with shop name
2. Wait for admin approval
3. Create product listings with categories, variants, and pricing
4. Manage active products
5. Respond to orders (accept/reject/ship)
6. Monitor order statuses

### For Administrators

1. Log into admin panel at `/admin/`
2. Manage user accounts and roles
3. Approve/reject seller requests
4. Create product categories
5. Monitor orders and transactions
6. Manage system-wide settings

## Key Components

### Custom User Model (`buyer/models.py`)
- Email-based authentication
- UUID primary key
- Role flags: `is_buyer`, `is_seller`
- EWU domain validation on registration

### Product Management (`products/models.py`)
- **Category**: Product categories with slugs and images
- **Product**: Core product model with variants support
- **ProductOption**: Additional product options with pricing
- **ColorVariant & SizeVariant**: Product attribute variants
- **Cart & CartItem**: Shopping cart functionality

### Order Processing (`orders/models.py`)
- Order status tracking (pending → delivered)
- Individual order item status management (seller-specific)
- Payment method and transaction ID tracking
- Automatic order status updates based on item statuses

### Seller Management (`seller/models.py`)
- SellerBanner: Branded storefront banners
- SellerRequest: Application workflow for new sellers

## Security Features

- **Email Domain Validation**: Only EWU students and staff can register
- **CSRF Protection**: Enabled on all forms
- **Password Security**: Django's password validators
- **Secure Payments**: SSLCommerz integration for PCI compliance
- **User Authentication**: Session-based with secure cookies

## Performance Considerations

- Database indexing on frequently queried fields (email, username, product slug)
- Image optimization through Pillow
- Static file serving for development
- Query optimization with select_related and prefetch_related where applicable

## Future Enhancements

- Product reviews and ratings
- Wishlist functionality
- Advanced search and filtering
- Recommendation engine
- Email notifications
- SMS alerts
- Inventory management
- Seller analytics dashboard
- Multiple payment gateway support

## Troubleshooting

### Database Issues
```bash
# Reset database (WARNING: deletes all data)
rm db.sqlite3
python manage.py migrate
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### Migration Issues
```bash
# Show migration status
python manage.py showmigrations

# Make migrations
python manage.py makemigrations
```

## Support

For issues, bugs, or feature requests, please contact the development team or create an issue in the repository.

## License

This project is developed for East West University. All rights reserved.