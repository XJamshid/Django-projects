from .models import Comments
from django import forms
class CommentAddForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=('body',)
        labels={
            'body':'',
        }
        widgets={
            'body':forms.TextInput(attrs={'class':'form-control','placeholder':'Add your comment here...'}),
        }