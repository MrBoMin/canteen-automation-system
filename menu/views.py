from django.shortcuts import render,get_object_or_404,redirect
from .models import MenuItem, Favorite, Review, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count 
from django.shortcuts import render
from .models import MenuItem, Category

def menu_list_view(request):
    search_query = request.GET.get('q', '')  # Get the search term from the query string
    categories = Category.objects.all()

    if search_query:
        menu_items = MenuItem.objects.filter(item_name__icontains=search_query)
    else:
        menu_items = MenuItem.objects.all()

    context = {
        'menu_items': menu_items,
        'categories': categories,
        'search_query': search_query,  # Pass the current search term to the template
    }
    return render(request, 'menu/menu.html', context)



def menu_detail_view(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    reviews = Review.objects.filter(menu_item=menu_item).select_related('user')
    is_favorite = (
        request.user.is_authenticated and 
        Favorite.objects.filter(user=request.user, menu_item=menu_item).exists()
    )

    context = {
        'menu_item': menu_item,
        'is_favorite': is_favorite,  # Add this to check favorite status
        'reviews' : reviews,
        'review_count': reviews.count()
    }

    return render(request, 'menu/menu_detail.html', context)


def toggle_favorite(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, menu_item=menu_item)

    if not created:
        favorite.delete()
    return redirect('menu:menu_detail', pk=pk)  



@login_required
def submit_review(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Check if the user has already reviewed this menu item
        existing_review = Review.objects.filter(user=request.user, menu_item=menu_item).first()

        if existing_review:
            # Update existing review
            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.save()
        else:
            # Create a new review
            Review.objects.create(
                user=request.user,
                menu_item=menu_item,
                rating=rating,
                comment=comment
            )

        return redirect('menu:menu_detail', pk=pk)

    return render(request, 'menu/menuDetail.html', {'menu_item': menu_item})