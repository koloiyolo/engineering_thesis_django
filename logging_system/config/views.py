from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages

from .forms import SettingsPage
from .models import Settings
from website.models import Log

# Create your views here.

def settings(request):
    print("Working")
    if request.user.is_authenticated:
        settings = Settings.load()
        form = SettingsPage(request.POST or None, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated successfully")
            return redirect('home')
        else:
            return render(request, 'settings.html', {'form': form})
    else:
        return redirect('home')

def reset_labels(request):
    if request.user.is_authenticated:
        Log.objects.update(label=None)
        return redirect('settings')
    else:
        return redirect('settings')

# validated function

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')