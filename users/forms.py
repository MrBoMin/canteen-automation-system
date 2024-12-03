from django import forms
from .models import User,Role
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-input mt-1 block w-full px-4 py-2 border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-input mt-1 block w-full px-4 py-2 border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        }),
    )


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'contact_number', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 p-1',
                'placeholder': 'Enter your username'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 p-1',
                'placeholder': 'Enter your password'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 p-1',
                'placeholder': 'Enter your email address'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 p-1',
                'placeholder': 'Enter your contact number'
            }),
        }
        

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')

        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one digit.')

        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')

        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')

        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Role.objects.get(role_name="user")
        if commit:
            user.save()
        return user



    


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'contact_number', 'bio', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }




# Custom password change form (optional)
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
