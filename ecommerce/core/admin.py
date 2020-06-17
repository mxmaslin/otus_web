from django.contrib import admin

from .models import Item, OrderItem, Order, Coupon, Refund, Address, UserProfile


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Предоставить возврат для заказов'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'ordered',
        # 'being_delivered',
        # 'received',
        # 'refund_requested',
        # 'refund_granted',
        'shipping_address',
        # 'payment',
        # 'coupon'
    ]
    list_display_links = [
        'user',
        'shipping_address',
        # 'payment',
        # 'coupon'
    ]
    list_filter = [
        'ordered',
        # 'being_delivered',
        # 'received',
        # 'refund_requested',
        # 'refund_granted'
    ]
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'house_number',
        'apartment_number',
        'shipping_zip',
        'default'
    ]
    list_filter = ['default']
    search_fields = [
        'user',
        'street_address',
        'house_number',
        'apartment_number',
        'shipping_zip'
    ]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass

