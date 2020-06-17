from django import forms


PAYMENT_CHOICES = (
    ('C', 'Кредитная карта'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(required=False)
    house_number = forms.CharField(required=False)
    apartment_number = forms.CharField(required=True)
    shipping_zip = forms.CharField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Промокод',
        'aria-label': 'Имя получателя',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField(label='Код заказа')
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Сообщение'
    )
    email = forms.EmailField()
