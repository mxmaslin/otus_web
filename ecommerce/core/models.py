import random
import string

from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import post_save


CATEGORY_CHOICES = (
    ('TS', 'Футболки'),
    ('SW', 'Спортивная одежда'),
    ('OW', 'Верхняя одежда')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    one_click_purchasing = models.BooleanField(
        default=False, verbose_name='Покупка в один клик'
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


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
    image = models.ImageField(verbose_name='Изображение')

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
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True
    )
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Товар добавлен в корзину
    2. Оформление заказа
    3. Платёж
    4. Доставка
    5. Получение
    6. Возврат
    '''

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        if total < 0:
            total = 0
        return total

    def __str__(self):
        return f'Заказ {self.user.username} {self.ordered_date}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    street_address = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=10, verbose_name='Дом, корпус')
    apartment_number = models.CharField(max_length=10, verbose_name='Номер квартиры')
    address_zip = models.CharField(max_length=6, blank=True)
    default = models.BooleanField(default=False)
    create_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Coupon(models.Model):
    code = models.CharField(max_length=15, verbose_name='Код')
    amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name='Скидка'
    )
    discarded = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    reason = models.TextField(verbose_name='Причина')
    accepted = models.BooleanField(default=False, verbose_name='Выполнен')
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
