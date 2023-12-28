from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import time

class UserWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    phone_number = models.CharField(max_length=10, unique=True, )
    pin = models.CharField(max_length=4)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        account_number = generate_unique_account_number()
        UserWallet.objects.create(user=instance,account_number=account_number) 
        
        

def generate_unique_account_number():
    return f"AC{int(time.time())}"                  

class Transaction(models.Model):
    sender = models.ForeignKey(UserWallet, related_name='sent_transactions', on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserWallet, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class PinChangeOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)    