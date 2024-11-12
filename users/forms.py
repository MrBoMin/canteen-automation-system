from django import forms
from .models import User


class LoginForm(forms.Form):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'}),
    )


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role', 'username', 'password','email', 'contact_number']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'form-control',  # This class will link to your CSS
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Enter your password',
                'class': 'form-control',
            }),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
