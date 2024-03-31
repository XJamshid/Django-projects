from .models import Product,ProductImage
from django import forms
class MultipleFileInput(forms.ClearableFileInput):
    #ClearableFileInput multiple filelarni templatega yuklash imkonini beradi
    #MultipleFileInput nomli class yaratdik
    allow_multiple_selected = True
    #HTML input dagi multiple bilan bir xil


class MultipleFileField(forms.FileField):
    #MultipleFileFiledni o'rgan!!!
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
class ProductCreateForm(forms.ModelForm):
    image=MultipleFileField()
    class Meta:
        model=Product
        fields=[
            'name',
            'brand',
            'description',
            'price',
            'count',
            'discount',
            'discount_price',
            'category',
            'image',
            'slug',
        ]