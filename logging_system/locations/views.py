from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib import messages

from website.functions import get_ping_graph

from .models import Location
from systems.models import System

# Create your views here.


def locations(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('home')

def edit(reques, pk):
    if request.user.is_authenticated:
        form = SystemForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Location added successfully")

                referer = request.META.get('HTTP_REFERER', '/')
                if referer: 
                    return redirect(referer)
                else:
                    return redirect('systems:add')
        else:
            return render(request, 'add_location.html', {'form': form})
        return render(request, 'add_location.html', {'form': form})
    else:
        return redirect('home')


def add(request):
    if request.user.is_authenticated:
        form = SystemForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Location added successfully")

                referer = request.META.get('HTTP_REFERER', '/')
                if referer: 
                    return redirect(referer)
                else:
                    return redirect('systems:add')
        else:
            return render(request, 'add_location.html', {'form': form})
        return render(request, 'add_location.html', {'form': form})
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
            return redirect('systems:add')
    else:
        return redirect('home')

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')
