from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'status', 'total_amount']  # Exclude 'order_date'
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
