from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Student, Teacher


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.is_student:
        Student.objects.get_or_create(user=instance)
    else:
        Teacher.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_student:
        instance.student.save()
    else:
        instance.teacher.save()

