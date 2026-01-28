from django import forms
from .models import Property

class PropertyCreateForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'address', 'url', 'image_url']
        

class PropertyUpdateForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'address', 'url', 'image_url']