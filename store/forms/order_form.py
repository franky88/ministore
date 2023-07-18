from django import forms
from store.models import OrderTransaction


class OrderTransaction(forms.ModelForm):
    class Meta:
        model = OrderTransaction
        fields = [
            'customer',
            'product',
            'price',
            'quantity',
            'money_tender',
            'is_paid'
        ]
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'money_tender': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_paid': forms.BooleanField(attrs={'class': 'form-control'}),
        }