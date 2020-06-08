from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView

from .models import Item, OrderItem, Order


class HomeView(ListView):
    model = Item
    template_name = 'home-page.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'В корзину добавлен ещё один экземпляр')
            return redirect('core:product', slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, 'Этот товар был добавлен в вашу корзину')
            return redirect('core:product', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.info(request, 'Этот товар был добавлен в вашу корзину')
        return redirect('core:product', slug=slug)
    return redirect('core:product', slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            messages.info(request, 'Этот товар был удалён из корзины')
        else:
            messages.info(request, 'Этого товара не было в вашей корзине')
            return redirect('core:product', slug=slug)
    else:
        messages.info(request, 'У вас пока нет заказов')
        return redirect('core:product', slug=slug)
    return redirect('core:product', slug=slug)


def checkout(request):
    return render(request, 'checkout.html')
