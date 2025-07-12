# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ClothingItem # Make sure to import User here

# --- FORM 1: For Listing Items (From Phase 2) ---
class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        # List the fields from the model that you want in the form
        fields = ['title', 'description', 'image', 'category', 'size', 'condition', 'points_value','price']
        

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'points_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Leave empty for swap-only'})
        }

# --- FORM 2: For User Signup (The one that was missing) ---
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # We add 'email' to the default signup form
        fields = UserCreationForm.Meta.fields + ('email',)

        # This loop applies the 'form-control' class to each field for Bootstrap styling
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs.update({'class': 'form-control'})
