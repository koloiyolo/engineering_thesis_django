from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required

from logging_system.functions import pagination
from .models import AuditLog
from config.models import Settings

# Create your views here.
@staff_member_required(login_url='/accounts/login/')
def logs(request, user=None):
    audit_logs = None
    q = request.GET.get('search', '')
    if user is not None:
        # Fix to display system audit logs
        if user == 0:
            user = None
        if q:
            audit_logs = AuditLog.objects.filter(
                Q(text__icontains=q) |
                Q(user__username__icontains=q),
                user = user
            ).order_by("-id")
        else:
            audit_logs = AuditLog.objects.filter(user=user).order_by("-id")
    else:
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