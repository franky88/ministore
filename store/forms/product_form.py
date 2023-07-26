from django import forms
from store.models import Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'cost', 'price', 'quantity', 'category', 'image'
        ]
        widgets = {
            # 'bar_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bar code', 'aria-label': 'bar code', 'aria-describedby': 'button-addon2'}),
            'name': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Name'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Cost'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Quantity'}),
            'category': forms.Select(attrs={'class': 'form-control mb-2', 'placeholder': 'Category'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'image'
        ]
        widgets = {
            # 'bar_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bar code', 'aria-label': 'bar code', 'aria-describedby': 'button-addon2'}),
            'name': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Name'}),
            'category': forms.Select(attrs={'class': 'form-control mb-2', 'placeholder': 'Category'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }