
from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm  
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password  
from django.contrib import messages
from menu.models import MenuItem,Favorite
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, CustomPasswordChangeForm
from .models import User
from orders.models import Order

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate the user using the email
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Or redirect to your desired page
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,'Registration successful! You can now log in.')
            return redirect('login')  
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')




def profile_view(request):
    # Fetch favorite menu items directly using select_related to avoid N+1 problem
    favorite_items = Favorite.objects.filter(user=request.user).select_related('menu_item')

    # Extract menu items directly from the related Favorite objects
    fav_items = [fav_item.menu_item for fav_item in favorite_items]

    context = {
        'favorite_items': fav_items,  # Pass a list of MenuItem objects to the template
    }
    return render(request, 'users/profile.html', context)



@login_required
def edit_user_info(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = UserEditForm(instance=user)

    return render(request, 'users/profile.html', {
        'user': user,
        'form': form,  # Pass the form to the template
    })

def my_orders(request):
    # Filter orders where the status is not 'Completed'
    favorite_items = Favorite.objects.filter(user=request.user).select_related('menu_item')

    # Extract menu items directly from the related Favorite objects
    fav_items = [fav_item.menu_item for fav_item in favorite_items]

    orders = Order.objects.filter(user=request.user).exclude(status='Completed').order_by('-order_date')
    context = {
        'favorite_items': fav_items,  # Pass a list of MenuItem objects to the template
        'orders' : orders
    }
    return render(request, 'users/my_orders.html', context)


def order_history(request):
    # Filter orders where the status is 'Completed'
    favorite_items = Favorite.objects.filter(user=request.user).select_related('menu_item')

    # Extract menu items directly from the related Favorite objects
    fav_items = [fav_item.menu_item for fav_item in favorite_items]

    # Filter orders that are completed, ordering them by the most recent order date
    orders = Order.objects.filter(user=request.user, status='Completed').order_by('-order_date')

    context = {
        'favorite_items': fav_items,  # Pass a list of MenuItem objects to the template
        'orders': orders
    }

    return render(request, 'users/order_history.html', context)



from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Redirect to profile page after successful password change
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'users/change_password.html', {'form': form})
