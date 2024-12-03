from django.db.models import Count
from django.utils.timezone import now
from django.db.models.functions import TruncDate
from orders.models import Order
from datetime import timedelta
from orders.models import OrderItem
from users.models import User
from menu.models import MenuItem
import json 
from django.db.models import F, Sum

def admin_dashboard_data(request):
    if request.path.startswith('/admin/'):  # Only apply to admin views
        # 1. Calculate total revenue (for completed orders)
        total_revenue = Order.objects.filter(status='Completed').aggregate(total=Sum('total_amount'))['total'] or 0

        # 2. Calculate total orders count (completed orders)
        total_orders = Order.objects.all().count()

        # 3. Calculate total menu items (assuming MenuItem is the model for menu items)
        total_menu = MenuItem.objects.count()

        # 4. Calculate total users (assuming User is the model for users)
        total_users = User.objects.count()

        # 5. Calculate total revenue by categories (using OrderItem and MenuItem)
        revenue_by_category = OrderItem.objects.filter(order__status='Completed') \
            .values('item__category__name') \
            .annotate(total_revenue=Sum(F('quantity') * F('item__price'))) \
            .order_by('item__category__name')

        # 6. Get the order count by day for the current month (group by order_date)
        today = now().date()
        start_of_month = today.replace(day=1)

        # Use TruncDate to group orders by day, ignoring time
        order_count_by_day = Order.objects.filter(order_date__gte=start_of_month) \
            .annotate(date_only=TruncDate('order_date')) \
            .values('date_only') \
            .annotate(order_count=Count('id')) \
            .order_by('date_only')

        # Format the order count by day for Chart.js
        order_count_data = [
            {
                'date': item['date_only'].strftime('%Y-%m-%d'),
                'order_count': item['order_count']
            }
            for item in order_count_by_day
        ]

        # Convert Decimal to float before passing to template for revenue_by_category
        revenue_by_category_data = [
            {
                'category_name': item['item__category__name'],
                'total_revenue': float(item['total_revenue'])  # Convert Decimal to float
            }
            for item in revenue_by_category
        ]

        recent_orders = Order.objects.order_by('-order_date')[:5]

        # Prepare context data for the template
        context = {
            'sub_card_1_value': total_revenue,
            'sub_card_2_value': total_orders,
            'sub_card_3_value': total_menu,
            'sub_card_4_value': total_users,
            'revenue_by_category': json.dumps(revenue_by_category_data),  # Pass data as JSON
            'order_count_by_day': json.dumps(order_count_data),  # Pass order count by day as JSON
            'recent_orders': recent_orders
        }

        return context
    return {}
