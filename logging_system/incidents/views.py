from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from logging_system.functions import pagination
from audit_log.models import AuditLog
from systems.models import System
from config.models import Settings
from .models import Incident, Comment
from .forms import CommentForm

# Create your views here.


@login_required
def incidents(request, tag=None, system=None):
    incidents = None
    q = request.GET.get('search', '')
    if tag is not None:
        if q:
            incidents = Incident.objects.filter(
                Q(system__name__icontains=q) |
                Q(ip__icontains=q) |
                Q(title__icontains=q) |
                Q(message__icontains=q),
                tag=tag,
            ).order_by("-id")
        else:
            incidents = Incident.objects.filter(tag=tag).order_by("-id")
    else:
        if q:
            incidents = Incident.objects.filter(
                Q(system__name__icontains=q) |
                Q(ip__icontains=q) |
                Q(title__icontains=q) |
                Q(message__icontains=q) |
                Q(tag__icontains=q)
            ).order_by("-id")
        else:
            incidents = Incident.objects.order_by("-id")
    
    page = pagination(incidents, request.GET.get("page"))
    systems = System.objects.filter(id__in=Incident.objects.values_list('system', flat=True).distinct())
    return render(request, 'incident/list.html', {
        'incidents': page,
        'systems': systems})


@login_required
def view(request, pk):
    incident = None
    try:
        incident = Incident.objects.get(id=pk)
    except Incident.DoesNotExist:
        return redirect('incidents:list')

    comments = Comment.objects.filter(incident=incident)
    form = CommentForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.incident = incident
            comment.save()
            AuditLog.objects.create(user=request.user, message=f"User {request.user} commented on incident '{incident}': {comment}")
            return redirect('incidents:view', incident.id )
        else:
            form = CommentForm()
    incident = Incident.objects.get(id=pk)
    comments = Comment.objects.filter(incident=incident)
    
    return render(request, 'incident/view.html', {
        'incident': incident,
        'comments': comments,
        'form': form
    })


@login_required
def remove(request, pk):
    delete_it = Incident.objects.get(id=pk)
    AuditLog.objects.create(user=request.user, message=f"User {request.user} removed incident {delete_it} successfully.")
    delete_it.delete()
    messages.success(request, "Incident removed successfully")
    return redirect(request.META.get('HTTP_REFERER', 'incidents:list'))

@login_required
def resolve(request, pk):
    incident = Incident.objects.get(id=pk)
    AuditLog.objects.create(user=request.user, message=f"User {request.user} resolved incident {incident}.")
    incident.user = request.user
    incident.save()
    messages.success(request, "Incident resolved successfully")
    return redirect(request.META.get('HTTP_REFERER', 'incidents:list'))


@login_required 
def report(request,frame=0, tag=None):
    AuditLog.objects.create(user=request.user, message=f"User {request.user} created incidents report.")

    start = (
        timezone.now() - timedelta(weeks=9999) if frame == 0 else
        timezone.now() - timedelta(days=30) if frame == 1 else
        timezone.now() - timedelta(days=7)
    )

    incidents = (
                Incident.objects.filter(date__gte=start)[:5000] if tag is None else 
                Incident.objects.filter(date__gte=start, tag=tag).order_by("id")[:5000]
                )

    current_date = timezone.now()
    return render(request, 'report/incident.html', {
                'date': current_date,
                'start': start,
                'user': request.user,
                'incidents': incidents
                })