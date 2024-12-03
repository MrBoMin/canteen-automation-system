from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from menu.models import MenuItem, Category, Review
from orders.models import OrderItem

@login_required
def home_view(request):
    # Fetching discounted items
    discounted_items = MenuItem.objects.filter(available=True).order_by('-price')[:8]  # Top 8 discounts
    popular_items = MenuItem.objects.filter(available=True).order_by('?')[:8]  # Random selection as popular

    # Fetching categories to display on the page 
    categories = Category.objects.all()
    reviews = Review.objects.select_related('menu_item', 'user').all().order_by('-created_at')[:5]

    # Fetch the most popular menu item based on number of orders (via OrderItem model)
    most_popular_item = MenuItem.objects.annotate(order_count=Count('orderitem')).order_by('-order_count').first()

    # Fetch the new menu item based on creation date
    new_menu_item = MenuItem.objects.filter(available=True).order_by('-created_at').first()

    
    context = {
        'discounted_items': discounted_items,
        'popular_items': popular_items,
        'categories': categories,
        'reviews': reviews,
        'most_popular_item': most_popular_item,
        'new_menu_item': new_menu_item
    }
    return render(request, 'pages/home.html', context)



def about_view(request):
    return render(request, 'pages/about.html')

def contact_view(request):
    return render(request, 'pages/contact.html')

