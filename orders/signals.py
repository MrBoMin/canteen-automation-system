from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from notification.models import Notification

@receiver(post_save, sender=Order)
def send_order_notifications(sender, instance, created, **kwargs):
    if created:
        # Notification for newly created order
        message = f"Your order #{instance.id} has been placed and is currently {instance.status}."
        Notification.objects.create(
            user=instance.user,
            message=message,
            order=instance
        )
    else:
        # Notification for order updates
        message = f"Your order #{instance.id} status has been updated to {instance.status}."
        if not Notification.objects.filter(order=instance, message=message).exists():
            Notification.objects.create(
                user=instance.user,
                message=message,
                order=instance
            )
