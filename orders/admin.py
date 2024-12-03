# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem

# admin.site.register(OrderItem)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order__id','item','quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'order_date', 'updated_at')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'id')
    ordering = ('-order_date',)
    list_per_page = 10

