from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from .models import Order , Customer
from django.contrib.auth.models import User
from django.conf import settings

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        customer =  Customer.objects.create(user=instance, email=instance.email)
        customer.save()

@receiver(post_save, sender=Order)
def send_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'New Order Created',
            f'Order {instance.id} has been created.',
            settings.EMAIL_HOST_USER,  
            [instance.customer.email], 
            fail_silently=False,
        )
