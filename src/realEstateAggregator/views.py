from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views import View

from realEstateAggregator.scrapper.tasks import run_scraper_task_async

from .forms import PropertyCreateForm, PropertyUpdateForm
from .models import Property


class HomeView(View):
    def get(self, request, *args, **kwargs):
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

class RunScraperView(View):
    def get(self, request, *args, **kwargs):
        return redirect('home')

    def post(self, request, *args, **kwargs):
        run_scraper_task_async.delay()

        return redirect('home')


class AddPropertyView(View):
    template_name = "add_property.html"

    def get(self, request, *args, **kwargs):
        form = PropertyCreateForm()
        context = {'form': form, 'title': 'Add Property'}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = PropertyCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property added successfully')
            return redirect('home')
        context = {'form': form, 'title': 'Add Property'}
        return render(request, self.template_name, context)


class UpdatePropertyView(View):
    template_name = 'add_property.html'

    def get(self, request, *args, **kwargs):
        property = Property.objects.get(id=kwargs.get('id'))
        form = PropertyUpdateForm(instance=property)
        context = {'form': form, 'title': 'Update Property'}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        property = Property.objects.get(id=kwargs.get('id'))
        form = PropertyUpdateForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully')
            return redirect('home')
        context = {'form': form, 'title': 'Update Property'}
        return render(request, self.template_name, context)


class DeletePropertyView(View):
    template_name = 'delete_property.html'

    def get(self, request, *args, **kwargs):
        property = Property.objects.get(id=kwargs.get('id'))
        context = {'property': property}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        property = Property.objects.get(id=kwargs.get('id'))
        property.delete()
        messages.success(request, 'Property deleted successfully')
        return redirect('home')
