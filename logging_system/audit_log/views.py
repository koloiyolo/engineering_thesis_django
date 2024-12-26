from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta

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
                Q(message__icontains=q) |
                Q(user__username__icontains=q),
                user = user
            ).order_by("-id")
        else:
            audit_logs = AuditLog.objects.filter(user=user).order_by("-id")
    else:
        if q:
            audit_logs = AuditLog.objects.filter(
                Q(message__icontains=q) |
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

@staff_member_required(login_url='/accounts/login/')
def report(request, frame=0, user=None):
    AuditLog.objects.create(user=request.user, message=f"User {request.user} created audit logs report.")

    start = (
        timezone.now() - timedelta(weeks=9999) if frame == 0 else
        timezone.now() - timedelta(days=30) if frame == 1 else
        timezone.now() - timedelta(days=7)
    )

    audit_log = (
                AuditLog.objects.filter(datetime__gte=start, user__isnull=True).order_by("id").order_by("-id")[:5000] if user == 0 else
                AuditLog.objects.filter(datetime__gte=start).order_by("-id")[:5000] if user is None else 
                AuditLog.objects.filter(datetime__gte=start, user=user).order_by("id").order_by("-id")[:5000]
                )

    current_date = timezone.now()
    return render(request, 'report/audit_log.html', {
                'date': current_date,
                'start': start,
                'audit_logs': audit_log,
                'user': request.user
                })