from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView, View

from .models import Item, OrderItem, Order, Address
from .forms import CheckoutForm, CouponForm, RefundForm


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'home-page.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'object': order}
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'У вас нет активных заказов')
            return redirect('/')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'Количество этого товара было обновлено.')
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, 'Этот товар был добавлен в вашу корзину.')
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'Этот товар был добавлен в вашу корзину.')
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, 'Этот товар был удалён из вашей корзины.')
            return redirect("core:order-summary")
        else:
            messages.info(request, 'Этого товара не было в вашей корзине.')
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, 'У вас нет активных заказов.')
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, 'Количество этого товара было обновлено.')
            return redirect("core:order-summary")
        else:
            messages.info(request, 'Этого товара не было в вашей корзине.')
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, 'У вас нет активных заказов.')
        return redirect("core:product", slug=slug)


def is_valid_form(values):
    for field in values:
        if not field:
            return False
    return True


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'shipping_address': shipping_address_qs[0]}
                )
            return render(self.request, 'checkout-page.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'У вас нет активных заказов')
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    print('yay' * 100)
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request,
                            'Адрес доставки по умолчанию недоступен'
                        )
                        return redirect('core:checkout')
                else:
                    street_address = form.cleaned_data.get(
                        'street_address')
                    house_number = form.cleaned_data.get(
                        'house_number')
                    apartment_number = form.cleaned_data.get(
                        'apartment_number')
                    shipping_zip = form.cleaned_data.get('shipping_zip')
                    if is_valid_form([
                        street_address,
                        house_number,
                        apartment_number,
                        shipping_zip
                    ]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=street_address,
                            house_number=house_number,
                            apartment_number=apartment_number,
                            shipping_zip=shipping_zip
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(
                            self.request,
                            'Пожалуйста, укажите адрес'
                        )
                        return redirect('core:checkout')

                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == 'C':
                    return redirect('core:payment', payment_option='credit_card')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, 'Выбран некорректный метод оплаты'
                    )
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, 'У вас нет активных заказов')
            return redirect("core:order-summary")
