from pydoc import describe

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import django_rq
import csv
from .models import *
from .forms import *
from .tasks import real_estate_scraper


def home(request):
    title = "Real Estate"
    description = "Click button to refresh the Real Estate list"
    records_qs = Property.objects.all().order_by("-id")

    paginator = Paginator(records_qs, 9)
    page_number = request.GET.get("page")
    records = paginator.get_page(page_number)
    
    context = {
        'title': title, 
        'description': description,
        'records': records,
    }
    
    return render(request, 'home.html', context)


def run_scrapper(request):
    real_estate_scraper()

    return redirect('home')


def add_property(request):
    form = PropertyCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Property added successfully')
        return redirect('home')
    context = {
        'form': form,
        'title': 'Add Property',
    }
    return render(request, "add_property.html", context)


def update_property(request, id):
    property = Property.objects.get(id=id)
    form = PropertyUpdateForm(instance=property)
    if request.method == "POST":
        form = PropertyUpdateForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully')
            return redirect('home')

    context = {
        'form': form,
    }
    return render(request, 'add_property.html', context)


def delete_property(request, id):
    property = Property.objects.get(id=id)
    if request.method == "POST":
        property.delete()
        messages.success(request, 'Property deleted successfully')
        return redirect('home')
    return render(request, 'delete_property.html')