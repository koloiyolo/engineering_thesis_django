from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q

from logging_system.functions import pagination
from .models import AuditLog
from config.models import Settings

# Create your views here.

def logs(request):
    if request.user.is_authenticated:

        audit_logs = None
        q = request.GET.get('search', '')
        if q:
            audit_logs = AuditLog.objects.filter(
                Q(text__icontains=q) |
                Q(user__username__icontains=q)
            ).order_by("-id")
        else:
            audit_logs = AuditLog.objects.order_by("-id")

        page = pagination(audit_logs, request.GET.get("page"))

        users = User.objects.all()

        data = {
            'audit_logs': page,
            'users': users
        }

        return render(request, 'audit_log/list.html' ,data)
        
    else:
        return redirect('home')

def user(request, pk):
    if request.user.is_authenticated:

        audit_logs = None
        if pk == 0:
            pk = None
        q = request.GET.get('search', '')
        if q:
            audit_logs = auditLog.filter(
                Q(text__icontains=q) |
                Q(user__username__icontains=q),
                user = pk
            ).order_by("-id")
        else:
            audit_logs = AuditLog.objects.filter(user=pk).order_by("-id")
        
        page = pagination(audit_logs, request.GET.get("page"))

        users = User.objects.all()

        data = {
            'audit_logs': page,
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