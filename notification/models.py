from django.db import models
from users.models import User
from orders.models import Order

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)  # Link to an order
    status = models.CharField(max_length=20, default='Unread')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
