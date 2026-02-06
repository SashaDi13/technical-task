# Register your models here.

from django.contrib import admin

from .forms import PropertyCreateForm
from .models import Property

# Register your models here.



class PropertyCreateAdmin(admin.ModelAdmin):
    list_display = ['object_id', 'title', 'price', 'currency', 'image_url']
    form = PropertyCreateForm
    list_filter = ['object_id']
    search_fields = ['object_id', 'title']

admin.site.register(Property, PropertyCreateAdmin)