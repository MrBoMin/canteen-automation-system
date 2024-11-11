from django.db import models
from menu.models import MenuItem
# Create your models here.
class Inventory(models.Model):
    item = models.OneToOneField(MenuItem, on_delete=models.CASCADE)
    stock = models.IntegerField()
    restock_level = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.item_name} - Stock: {self.stock}"
