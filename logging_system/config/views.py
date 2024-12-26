from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from .forms import SettingsPage
from .models import Settings
from audit_log.models import AuditLog

# Create your views here.
@staff_member_required(login_url='/accounts/login/')
def settings(request):
    print("Working")
    if request.user.is_authenticated:
        settings = Settings.load()
        form = SettingsPage(request.POST or None, instance=settings)
        if form.is_valid():
            form.save()
            AuditLog.objects.create(user=request.user, message=f"User {request.user} updated settings.")
            messages.success(request, "Settings updated successfully")
            return redirect('home')
        else:
            return render(request, 'misc/settings.html', {'form': form})
    else:
        return redirect('home')
