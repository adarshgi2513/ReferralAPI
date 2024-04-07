from django.db import models
# Create your models here.
from django.utils import timezone
from django.dispatch import receiver
import uuid
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    referral_code = models.CharField(max_length=20, blank=True, null=True)
    registration_timestamp = models.DateTimeField(default=timezone.now)
    referral_points = models.IntegerField(default=0)
    myreferral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)

   
    
@receiver(post_save, sender=User)
def generate_referral_code(sender, instance, created, **kwargs):
    if created and not instance.myreferral_code:
        # Generate a unique referral code
        referral_code = str(uuid.uuid4())[:8].replace('-', '').upper()  # Generate a random code
        while User.objects.filter(myreferral_code=referral_code).exists():  # Ensure uniqueness
            referral_code = str(uuid.uuid4())[:8].replace('-', '').upper()
        # Save the generated referral code to the user's myreferral_code field
        instance.myreferral_code = referral_code
        instance.save()