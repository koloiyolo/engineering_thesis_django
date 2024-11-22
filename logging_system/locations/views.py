from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib import messages

from config.models import Settings
from .models import Location
from .forms import LocationForm
from systems.models import System

# Create your views here.


def locations(request):
    if request.user.is_authenticated:
        locations = Location.objects.all().order_by("id")
        for location in locations:
            location.systems = System.objects.filter(location=location).count()
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(locations, items_per_page)
        page_number = request.GET.get("page")
        page_locations = paginator.get_page(page_number)
        
        return render(request, 'location/list.html', {'locations': page_locations})
    else:
        return redirect('home')

def edit(request, pk):
    if request.user.is_authenticated:
        update_it = Location.objects.get(id=pk)
        form = LocationForm(request.POST or None, instance=update_it)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Location edited successfully")
                # return redirect('locations:list')
                return redirect('home')
                    
        else:
            return render(request, 'location/edit.html', {'form': form})
    else:
        return redirect('home')


def add(request):
    if request.user.is_authenticated:
        form = LocationForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Location added successfully")
                return redirect('systems:add')
        else:
            return render(request, 'location/add.html', {'form': form})
        return render(request, 'location/add.html', {'form': form})
    else:
        return redirect('home')

def remove(request, pk):
    if request.user.is_authenticated:
        delete_it = Location.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Location removed successfully")
        referer = request.META.get('HTTP_REFERER', '/')
        if referer: 
            return redirect(referer)
        else:
            return redirect('locations:list')
    else:
        return redirect('home')

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')
