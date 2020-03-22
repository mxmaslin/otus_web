from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class ProfileMixin(models.Model):
    profile_id = models.AutoField(primary_key=True)
    phone = PhoneNumberField()
    photo = models.ImageField(upload_to=f'faces/{phone}')

