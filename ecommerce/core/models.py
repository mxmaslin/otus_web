from django.conf import settings
from django.db import models
from django.shortcuts import reverse


CATEGORY_CHOICES = (
    ('S', 'Футболки'),
    ('SW', 'Спортивная одежда'),
    ('OW', 'Верхняя одежда')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Item(models.Model):
    title = models.CharField(
        max_length=100, verbose_name='Название'
    )
    price = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name='Цена'
    )
    discount_price = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True,
        verbose_name='Цена со скидкой'
    )
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=2, verbose_name='Категория'
    )
    label = models.CharField(
        choices=LABEL_CHOICES, max_length=1, verbose_name='Метка'
    )
    slug = models.SlugField(verbose_name='Идентификатор')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:product', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse('core:remove-from-cart', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class OrderItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    ordered = models.BooleanField(default=False, verbose_name='Товар заказан')
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, verbose_name='Товар'
    )
    quantity = models.IntegerField(
        default=1, verbose_name='Количество в заказе'
    )

    def __str__(self):
        return f'{self.item.title}: {self.quantity}'

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem, verbose_name='Товары')
    start_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата начала заказа'
    )
    ordered_date = models.DateTimeField(verbose_name='Дата формирования заказа')
    ordered = models.BooleanField(default=False, verbose_name='Заказ сделан')
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def __str__(self):
        return f'Заказ {self.user.username} {self.ordered_date}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    street_address = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=10, verbose_name='Дом, корпус')
    apartment_number = models.CharField(max_length=10, verbose_name='Номер квартиры')
    shipping_zip = models.CharField(max_length=6)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
