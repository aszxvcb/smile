from django import forms
from .models import Photo

class PhotoPost(forms.ModelForm):
    class Meta:
        model = Photo
        # fields = ['owner', 'image']
        fields = ['image']