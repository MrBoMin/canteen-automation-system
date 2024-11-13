
from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm  
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password  
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']  # Use 'username' for email here
            password = form.cleaned_data['password']
            
            # Authenticate user using the custom backend
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)  # Logs the user in
                next_url = request.GET.get('next')  # Get next parameter from query string
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('home')  # Redirect to home page
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

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


def logout_view(request):
    logout(request)
    return redirect('login')
