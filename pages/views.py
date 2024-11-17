from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from menu.models import MenuItem, Category


# @login_required
def home_view(request):
    # Fetching menu items
    discounted_items = MenuItem.objects.filter(available=True).order_by('-price')[:8]  # Example: Top 8 discounts
    popular_items = MenuItem.objects.filter(available=True).order_by('?')[:8]  # Random selection as popular

    # Fetching categories to display on the page 
    categories = Category.objects.all()
    
    context = {
        'discounted_items': discounted_items,
        'popular_items': popular_items,
        'categories': categories,
    }
    return render(request, 'pages/home.html', context)


def about_view(request):
    return render(request, 'pages/about.html')

def contact_view(request):
    return render(request, 'pages/contact.html')



def header_view(request):
    return render(request, 'header.html')

def footer_view(request):
    return render(request, 'footer.html')