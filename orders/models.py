from django.db import models
from users.models import User
from menu.models import MenuItem

from django.db import models
from users.models import User
from menu.models import MenuItem


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.item.item_name} - {self.quantity} pcs"

    def save(self, *args, **kwargs):
        # Automatically set the price based on the item
        if not self.price:
            self.price = self.item.price
        super().save(*args, **kwargs)



class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Processing', 'Processing'),
        ('Ready to Pickup', 'Ready to Pickup'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = (
        ('Cash on Pickup', 'Cash on Pickup'),
        ('Card Payment', 'Card Payment'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=20, null=True, blank=True)
    payment_status = models.BooleanField(default=False)  # False = not paid, True = paid
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.get_status_display()}"

    def calculate_total_amount(self):
        self.total_amount = sum(item.subtotal for item in self.order_items.all())
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.item_name} (Order #{self.order.id})"

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically calculate the subtotal
        based on price and quantity.
        """
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)
        self.order.calculate_total_amount()
