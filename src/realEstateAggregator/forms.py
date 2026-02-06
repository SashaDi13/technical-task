import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Property


class PropertyCreateForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            "title", "price", "url", "currency", 
            "address", "description", "image_url"
        ]

    def clean_url(self):
        url = self.cleaned_data.get("url")
        if not url:
            raise ValidationError("URL обов'язковий для створення запису")

        pattern = r'/(\d+)-[^/]+/?$'
        if not re.search(pattern, url):
            raise ValidationError(
                "URL має містити правильний формат, наприклад: /<object_id>-назва/..."
            )
        return url


    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.object_id:
            instance.object_id = instance.extract_object_id()
        if commit:
            instance.save()
        return instance
        

class PropertyUpdateForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ["title", "price", "currency", "address", "description", "image_url"]