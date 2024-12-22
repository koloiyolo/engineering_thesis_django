from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from logging_system.functions import pagination
from config.models import Settings
from .models import Location
from .forms import LocationForm
from systems.models import System
from audit_log.models import AuditLog

# Create your views here.


@login_required
def locations(request):
    locations = Location.objects.all().order_by("id")
    for location in locations:
        location.systems = System.objects.filter(location=location).count()
    
    page = pagination(locations, request.GET.get("page"))
    
    return render(request, 'location/list.html', {'locations': page})


@login_required
def edit(request, pk):
    update_it = Location.objects.get(id=pk)
    form = LocationForm(request.POST or None, instance=update_it)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            AuditLog.objects.create(user=request.user, text=f"{request.user} updated location {update_it} successfully.")
            messages.success(request, "Location edited successfully")
            # return redirect('locations:list')
            return redirect('home')
                
    else:
        return render(request, 'location/edit.html', {'form': form})


@login_required
def add(request):
    form = LocationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            add_record = form.save()
            AuditLog.objects.create(user=request.user, text=f"{request.user} created location {add_record} successfully.")
            messages.success(request, "Location added successfully")
            return redirect('systems:add')
    else:
        return render(request, 'location/add.html', {'form': form})
    return render(request, 'location/add.html', {'form': form})

def remove(request, pk):
    delete_it = Location.objects.get(id=pk)
    AuditLog.objects.create(user=request.user, text=f"{request.user} removed location {delete_it} successfully.")
    delete_it.delete()
    messages.success(request, "Location removed successfully")
    referer = request.META.get('HTTP_REFERER', '/')
    if referer: 
        return redirect(referer)
    else:
        return redirect('locations:list')

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')
