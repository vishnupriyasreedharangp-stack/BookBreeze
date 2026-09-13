from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignUpForm
from .models import (
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    Product,
    Wishlist,
    WishlistItem,
)


def home(request):
    return render(
        request,
        'home.html',
        {
            'categories': Category.objects.all(),
            'featured_products': Product.objects.filter(
                is_active=True
            )[:8],
        }
    )


def index(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', '').strip()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )

    if category_slug:
        products = products.filter(
            category__slug=category_slug
        )

    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by(
            '-created_at',
            '-id'
        )

    return render(
        request,
        'index.html',
        {
            'products': products,
            'categories': categories,
            'query': query,
            'selected_category': category_slug,
            'selected_sort': sort,
        }
    )


def detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(
        id=product.id
    )[:4]

    return render(
        request,
        'product_detail.html',
        {
            'product': product,
            'related_products': related_products,
        }
    )


def new(request):
    products = Product.objects.filter(
        is_active=True
    ).order_by(
        '-created_at',
        '-id'
    )

    return render(
        request,
        'new_arrivals.html',
        {
            'products': products,
        }
    )


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            Cart.objects.create(
                user=user
            )

            login(
                request,
                user
            )

            messages.success(
                request,
                'Your PyShop Books account has been created!'
            )

            return redirect('home')

    else:
        form = SignUpForm()

    return render(
        request,
        'registration/signup.html',
        {
            'form': form
        }
    )


def user_logout(request):
    logout(request)

    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect('home')


@login_required
def cart(request):
    user_cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = user_cart.items.select_related(
        'product'
    )

    return render(
        request,
        'cart.html',
        {
            'cart': user_cart,
            'items': items
        }
    )


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    if product.stock <= 0:
        messages.error(
            request,
            f'{product.name} is currently out of stock.'
        )

        return redirect(
            'product_detail',
            product_id=product.id
        )

    user_cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, item_created = CartItem.objects.get_or_create(
        cart=user_cart,
        product=product,
        defaults={
            'quantity': 1
        },
    )

    if not item_created:

        if item.quantity >= product.stock:
            messages.warning(
                request,
                'You cannot add more than the available stock.'
            )

            return redirect('cart')

        item.quantity += 1
        item.save()

    messages.success(
        request,
        f'{product.name} added to your cart.'
    )

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    messages.success(
        request,
        'Item removed from your cart.'
    )

    return redirect('cart')


@login_required
def wishlist(request):
    user_wishlist, created = Wishlist.objects.get_or_create(
        user=request.user
    )

    items = user_wishlist.items.select_related(
        'product',
        'product__category'
    )

    return render(
        request,
        'wishlist.html',
        {
            'wishlist': user_wishlist,
            'items': items
        }
    )


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    user_wishlist, created = Wishlist.objects.get_or_create(
        user=request.user
    )

    item, item_created = WishlistItem.objects.get_or_create(
        wishlist=user_wishlist,
        product=product
    )

    if item_created:
        messages.success(
            request,
            f'{product.name} added to your wishlist.'
        )
    else:
        messages.info(
            request,
            f'{product.name} is already in your wishlist.'
        )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'wishlist'
        )
    )


@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(
        WishlistItem,
        id=item_id,
        wishlist__user=request.user
    )

    product_name = item.product.name

    item.delete()

    messages.success(
        request,
        f'{product_name} removed from your wishlist.'
    )

    return redirect('wishlist')


@login_required
def checkout(request):
    user_cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = list(
        user_cart.items.select_related('product')
    )

    if not items:
        messages.warning(
            request,
            'Your cart is empty.'
        )

        return redirect('cart')

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    if request.method == 'POST':

        with transaction.atomic():

            for item in items:

                product = Product.objects.select_for_update().get(
                    id=item.product.id
                )

                if not product.is_active:
                    messages.error(
                        request,
                        f'{product.name} is no longer available.'
                    )

                    return redirect('cart')

                if product.stock < item.quantity:
                    messages.error(
                        request,
                        f'Not enough stock available for '
                        f'{product.name}.'
                    )

                    return redirect('cart')

            last_order = Order.objects.order_by(
                '-id'
            ).first()

            if last_order:
                next_number = last_order.id + 1
            else:
                next_number = 1

            order_number = f'PYSHOP-{next_number:06d}'

            order = Order.objects.create(
                user=request.user,
                order_number=order_number,
                total_amount=total,
                status='confirmed',
            )

            for item in items:

                product = Product.objects.select_for_update().get(
                    id=item.product.id
                )

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    price=product.price,
                    quantity=item.quantity,
                    subtotal=product.price * item.quantity,
                )

                product.stock -= item.quantity
                product.save()

            user_cart.items.all().delete()

        messages.success(
            request,
            f'Order {order.order_number} placed successfully!'
        )

        return redirect(
            'order_success',
            order_id=order.id
        )

    return render(
        request,
        'checkout.html',
        {
            'cart': user_cart,
            'items': items,
            'total': total
        }
    )


@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'order_success.html',
        {
            'order': order
        }
    )


@login_required
def order_history(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'order_history.html',
        {
            'orders': orders
        }
    )


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related(
            'items__product'
        ),
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'order_detail.html',
        {
            'order': order
        }
    )