from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from config.models import Settings
from django.core.paginator import Paginator
from django.db.models import Q
from .models import AuditLog
from config.models import Settings

# Create your views here.

def logs(request):
    if request.user.is_authenticated:

        audit_logs = None
        q = request.GET.get('search', '')
        if q:
            audit_logs = auditLog.filter(
                Q(text__icontains=q) |
                Q(user__username__icontains=q)
            ).order_by("-id")
        else:
            audit_logs = AuditLog.objects.order_by("-id")

        items_per_page = Settings.load().items_per_page
        paginator = Paginator(audit_logs, items_per_page)
        page_number = request.GET.get("page")
        page_items = paginator.get_page(page_number)
        users = User.objects.all()

        data = {
            'audit_logs': page_items,
            'users': users
        }

        return render(request, 'audit_log/list.html' ,data)
        
    else:
        return redirect('home')

def user(request, pk):
    if request.user.is_authenticated:

        audit_logs = None
        q = request.GET.get('search', '')
        if q:
            audit_logs = auditLog.filter(
                Q(text__icontains=q) |
                Q(user__username__icontains=q),
                user = pk
            ).order_by("-id")
        else:
            audit_logs = AuditLog.objects.filter(user=pk).order_by("-id")
        
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(audit_logs, items_per_page)
        page_number = request.GET.get("page")
        page_items = paginator.get_page(page_number)
        users = User.objects.all()

        data = {
            'audit_logs': page_items,
            'users': users
        }

        return render(request, 'audit_log/list.html' ,data)

    else:
        return redirect('home')

# validated function

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')