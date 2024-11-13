from django import forms
from .models import User,Role
import re
from django.core.exceptions import ValidationError

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
        fields = ['username', 'password','email', 'contact_number']
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password') 

        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
            
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one digit.')

            # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')

            # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')

        return password


    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Role.objects.get(role_name="user")
        if commit:
            user.save()
        return user