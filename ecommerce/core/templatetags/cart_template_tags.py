from django import template
from django.db.models import Sum

from core.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False).annotate(
            num=Sum('items__quantity')
        )
        if qs.exists():
            return qs[0].num or 0
    return 0
