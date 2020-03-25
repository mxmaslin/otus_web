from django.core.mail import send_mail


class SendMailMixin:
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], **kwargs)