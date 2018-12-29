from webbrowser import register

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    gender = models.CharField(
        max_length=2, choices=(('M', 'مرد'), ('F', 'زن')), default='M'
    )
    picture = models.FileField(blank=True, null=True, upload_to="")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Meeting(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    date = models.DateTimeField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    capacity = models.IntegerField()

    class Meta:
        verbose_name_plural = "Teacher Free Times"