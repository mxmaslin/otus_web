from django import forms
from django.core import mail


class FeedbackForm(forms.Form):
    recipient = forms.EmailField(label='Получатель')
    subject = forms.CharField(label='Тема письма', max_length=100)
    message = forms.CharField(label='Содержание письма', widget=forms.Textarea)
    sender = forms.EmailField(label='Отправитель')
    cc_myself = forms.BooleanField(label='Отправить копию себе', required=False)

    def send_email(self):
        recipient = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        sender = self.cleaned_data['sender']
        cc_myself = self.cleaned_data['cc_myself']
        recipients = [recipient, sender] if cc_myself else [recipient]
        with mail.get_connection() as connection:
            mail.EmailMessage(
                subject, message, sender, recipients, connection=connection,
            ).send()
