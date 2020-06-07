from django.conf import settings
from django.db import models
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
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

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class OrderItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        blank=True,
        null=True
    )
    ordered = models.BooleanField(default=False, verbose_name='Заказ сделан')
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, verbose_name='Товар'
    )
    quantity = models.IntegerField(
        default=1, verbose_name='Количество в заказе'
    )

    def __str__(self):
        return f'{self.item.title}: {self.quantity}'

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    items = models.ManyToManyField(OrderItem, verbose_name='Товары')
    start_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата начала заказа'
    )
    ordered_date = models.DateTimeField(verbose_name='Дата формирования заказа')
    ordered = models.BooleanField(default=False, verbose_name='Заказ сделан')

    def __str__(self):
        return f'Заказ {self.user.username} {self.ordered_date}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
