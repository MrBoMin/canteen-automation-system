from django.db import models
from orders.models import Order

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50, default='Pending')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
