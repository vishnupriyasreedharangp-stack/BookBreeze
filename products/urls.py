from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'products/',
        views.index,
        name='products'
    ),

    path(
        'products/<int:product_id>/',
        views.detail,
        name='product_detail'
    ),

    path(
        'products/new/',
        views.new,
        name='new_arrivals'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/remove/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'wishlist/',
        views.wishlist,
        name='wishlist'
    ),

    path(
        'wishlist/add/<int:product_id>/',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),

    path(
        'wishlist/remove/<int:item_id>/',
        views.remove_from_wishlist,
        name='remove_from_wishlist'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'orders/',
        views.order_history,
        name='order_history'
    ),

    path(
        'orders/<int:order_id>/',
        views.order_detail,
        name='order_detail'
    ),

    path(
        'order/success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),
]