from django import forms
from .models import Category

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields=[
            'name',
            'slug',
        ]