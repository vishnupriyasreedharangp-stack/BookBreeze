from django.contrib import admin

from .models import (
    Category,
    Offer,
    Order,
    OrderItem,
    Product,
)


# ---------------------------------------------------------
# CATEGORY
# ---------------------------------------------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )

    prepopulated_fields = {
        'slug': ('name',)
    }

    search_fields = (
        'name',
    )


# ---------------------------------------------------------
# PRODUCT / BOOK
# ---------------------------------------------------------

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'category',
        'price',
        'stock',
        'is_active',
        'created_at',
    )

    list_filter = (
        'category',
        'is_active',
    )

    search_fields = (
        'name',
        'author',
        'isbn',
    )

    list_editable = (
        'price',
        'stock',
        'is_active',
    )

    ordering = (
        '-created_at',
    )


# ---------------------------------------------------------
# OFFER
# ---------------------------------------------------------

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'description',
        'discount',
        'active',
        'valid_from',
        'valid_until',
    )

    list_filter = (
        'active',
    )

    search_fields = (
        'code',
        'description',
    )


# ---------------------------------------------------------
# ORDER ITEM INLINE
# ---------------------------------------------------------

class OrderItemInline(admin.TabularInline):
    model = OrderItem

    extra = 0

    fields = (
        'product',
        'product_name',
        'price',
        'quantity',
        'subtotal',
    )

    readonly_fields = (
        'product_name',
        'price',
        'subtotal',
    )


# ---------------------------------------------------------
# ORDER
# ---------------------------------------------------------

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'user',
        'total_amount',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'order_number',
        'user__username',
        'user__email',
    )

    readonly_fields = (
        'order_number',
        'user',
        'total_amount',
        'created_at',
        'updated_at',
    )

    ordering = (
        '-created_at',
    )

    inlines = (
        OrderItemInline,
    )


# ---------------------------------------------------------
# ORDER ITEM
# ---------------------------------------------------------

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        'order',
        'quantity',
        'price',
        'subtotal',
    )

    list_filter = (
        'order__status',
    )

    search_fields = (
        'product_name',
        'order__order_number',
    )

    readonly_fields = (
        'product_name',
        'price',
        'quantity',
        'subtotal',
    )

    ordering = (
        '-order__created_at',
    )