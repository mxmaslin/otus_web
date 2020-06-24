from django import forms


class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    house_number = forms.CharField()
    apartment_number = forms.CharField()
    address_zip = forms.CharField(required=False)
    set_default_address = forms.BooleanField(required=False)


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
