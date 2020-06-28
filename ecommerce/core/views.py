from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
    Item, OrderItem, Order, Address, Coupon, Refund, CATEGORY_CHOICES
)
from .forms import CheckoutForm, CouponForm, RefundForm


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'home-page.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.setdefault('categories', CATEGORY_CHOICES)
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'object': order}
            return render(self.request, 'order-summary-page.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'У вас нет активных заказов')
            return redirect('/')


def wear_category(request, category):
    wear = Item.objects.filter(category=category)
    return render(
        request,
        'home-page.html',
        {'object_list': wear, 'categories': CATEGORY_CHOICES}
    )


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
        order = order_qs.first()
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity = F('quantity') + 1
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
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            ).first()
            order_item.delete()
            if order.items.all().count() < 1:
                order.delete()
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
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            ).first()
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            if len(order.items.all()) < 1:
                order.delete()
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
            address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            ).order_by('-create_dt')
            if address_qs.exists():
                context.update({'default_address': address_qs.first()})
            return render(self.request, 'checkout-page.html', context)
        except Order.DoesNotExist:
            messages.info(self.request, 'У вас нет активных заказов')
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                house_number = form.cleaned_data.get('house_number')
                apartment_number = form.cleaned_data.get('apartment_number')
                address_zip = form.cleaned_data.get('address_zip')
                if is_valid_form([
                    street_address,
                    house_number,
                    apartment_number,
                ]):
                    shipping_address = Address(
                        user=self.request.user,
                        street_address=street_address,
                        house_number=house_number,
                        apartment_number=apartment_number,
                        address_zip=address_zip
                    )
                    shipping_address.save()
                    order.shipping_address = shipping_address
                    order.save()
                    if form.cleaned_data.get('set_default_address'):
                        shipping_address.default = True
                        shipping_address.save()
                else:
                    messages.info(self.request, 'Пожалуйста, укажите адрес')
                    return redirect('core:checkout')
                return redirect('core:payment', order_pk=order.pk)
            else:
                messages.info(
                    self.request, 'Пожалуйста, укажите требуемые данные'
                )
                return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.warning(self.request, 'У вас нет активных заказов')
            return redirect("core:order-summary")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, 'Купон не существует')
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, ordered=False)
                coupon = get_coupon(self.request, code)
                order.coupon = coupon
                order.save()
                coupon.discarded = True
                coupon.save()
                messages.success(self.request, 'Купон успешно добавлен')
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, 'У вас нет активного заказа')
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {'form': form}
        return render(self.request, "request-refund-page.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                messages.info(self.request, 'Запрос на возврат получен.')
                return redirect("core:request-refund")

            except Order.DoesNotExist:
                messages.info(self.request, 'Этот заказ не существует.')
                return redirect("core:request-refund")


@login_required
def payment(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    order.ordered = True
    order.save()
    return render(request, 'payment-page.html', {})
