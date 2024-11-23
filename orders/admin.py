from django.contrib import admin
from .models import Order, OrderItem
from notification.models import Notification  # Import the Notification model

admin.site.register(OrderItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'order_date')  # Changed 'created_at' to 'order_date'
    list_filter = ('status',)
    actions = ['mark_as_confirmed', 'mark_as_processing', 'mark_as_ready_to_pickup']

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
        for order in queryset:
            Notification.objects.create(
                user=order.user,
                message=f"Your order #{order.id} has been marked as Confirmed."
            )
        self.message_user(request, "Selected orders have been marked as Confirmed.")
    mark_as_confirmed.short_description = "Mark selected orders as Confirmed"

    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
        for order in queryset:
            Notification.objects.create(
                user=order.user,
                message=f"Your order #{order.id} is now Processing."
            )
        self.message_user(request, "Selected orders have been marked as Processing.")
    mark_as_processing.short_description = "Mark selected orders as Processing"

    def mark_as_ready_to_pickup(self, request, queryset):
        queryset.update(status='ready_to_pickup')
        for order in queryset:
            Notification.objects.create(
                user=order.user,
                message=f"Your order #{order.id} is Ready to Pickup."
            )
        self.message_user(request, "Selected orders have been marked as Ready to Pickup.")
    mark_as_ready_to_pickup.short_description = "Mark selected orders as Ready to Pickup"


