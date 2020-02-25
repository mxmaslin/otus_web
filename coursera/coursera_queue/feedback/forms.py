from django import forms


class FeedbackForm(forms.Form):
    recipient = forms.EmailField(label='Получатель')
    subject = forms.CharField(label='Тема письма', max_length=100)
    message = forms.CharField(label='Содержание письма', widget=forms.Textarea)
    sender = forms.EmailField(label='Отправитель')
    cc_myself = forms.BooleanField(label='Отправить копию себе', required=False)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass