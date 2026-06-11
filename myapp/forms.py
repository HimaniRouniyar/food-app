from .models import Item
from django import forms

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name','item_desc','item_price',
                  'item_image']
        
        widgets = {
            'item_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter food name'
            }),

            'item_desc': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description',
                'rows': 3
            }),

            'item_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),

            'item_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }