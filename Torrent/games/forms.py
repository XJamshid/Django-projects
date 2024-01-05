from .models import Game
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

class GameCreateForm(forms.ModelForm):
    screenshots=MultipleFileField()
    class Meta:
        model=Game
        fields=[
            'name',
            'release_date',
            'category',
            'platform',
            'developer',
            'os',
            'processor',
            'ram',
            'video_card',
            'disk_space',
            'about',
            'poster',
            'trailer',
            'screenshots',
            'file',
        ]
"""        widgets = {
            'screenshots': forms.ClearableFileInput(attrs={'class': 'form-control','allow_multiple_selected': True}),
        }"""