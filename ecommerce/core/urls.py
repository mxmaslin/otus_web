from django.urls import path
from .views import (
    HomeView,
    wear_category,
    CheckoutView,
    ItemDetailView,
    OrderSummaryView,
    AddCouponView,
    RequestRefundView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    payment
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('wear_category/<category>/', wear_category, name='wear-category'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/',
         remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('payment/', payment, name='payment')
]
