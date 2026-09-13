# BookBreeze Books 📚

A full-stack online bookstore built with Python and Django.

BookBreeze Books is a portfolio project demonstrating Django web development, database design, authentication, e-commerce workflows, and responsive frontend development.

## 🚀 Features

### User Authentication
- User registration
- Login and logout
- Authenticated user sessions
- User-specific cart, wishlist, and orders

### Book Catalogue
- Browse available books
- Book categories
- Search books by title, author, or ISBN
- Filter books by category
- Sort books by:
  - Newest
  - Price: Low to High
  - Price: High to Low
  - Name
- Book detail pages
- New Arrivals section

### Shopping Cart
- Add books to cart
- Remove books from cart
- Quantity management
- Automatic cart totals
- Stock availability validation

### Wishlist
- Add books to wishlist
- Remove books from wishlist
- User-specific wishlist
- Prevent duplicate wishlist items

### Checkout & Orders
- Secure checkout flow
- Stock validation before order creation
- Transaction-based order processing
- Automatic stock reduction
- Order number generation
- Order history
- Detailed order pages
- Order status tracking

### Django Admin
- Manage books
- Manage categories
- Manage offers
- View orders
- View order items
- Manage application data through Django Admin

## 🛠️ Tech Stack

### Backend
- Python 3.12
- Django 5.2.7
- Django ORM
- SQLite

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Bootstrap Icons
- Google Fonts

### Development Tools
- Git
- GitHub
- Django Management Commands

## 🗂️ Project Structure

```text
PyShop-master/
│
├── manage.py
│
├── products/
│   ├── migrations/
│   ├── management/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── pyshop/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
│   └── books/
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── index.html
│   ├── product_detail.html
│   ├── new_arrivals.html
│   ├── cart.html
│   ├── wishlist.html
│   ├── checkout.html
│   ├── order_history.html
│   ├── order_detail.html
│   └── registration/
│
├── .gitignore
├── requirements.txt
├── README.md
└── pyshop-app.png