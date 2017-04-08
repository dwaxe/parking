from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class ParkingSpot(models.Model):
    address = models.CharField(max_length=100, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    is_reserved = models.BooleanField(default=False)
    reserved_until = models.DateTimeField(default=timezone.now)
    reservation_owner = models.ForeignKey('auth.User', blank=True, null=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=1)
    
    def clean(self):
        if self.reserved_until <= timezone.now():
            self.is_reserved = False
            self.reservation_owner = None
        else:
            self.is_reserved = True

    def __str__(self):
        return "{} {}".format(self.lat, self.lng)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=16, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
