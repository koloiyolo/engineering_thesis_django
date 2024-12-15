from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from logging_system.functions import pagination
from audit_log.models import AuditLog
from systems.models import System
from config.models import Settings
from .models import Incident, Comment
from .forms import CommentForm

# Create your views here.

# validated function

def incidents(request, tag=None, system=None):
    if request.user.is_authenticated:

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
            if incidents.count() == 0:
                return redirect('incidents:list') 
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
    else:
        return redirect('home') 

def view(request, pk):
    if request.user.is_authenticated:
        incident = Incident.objects.get(id=pk)
        comments = Comment.objects.filter(incident=incident)
        form = CommentForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.incident = incident
                comment.save()
                AuditLog.objects.create(user=request.user, text=f"{request.user} commented on incident '{incident}': {comment}")
                return redirect('incidents:view', incident.id)
            else:
                form = CommentForm()

        incident = Incident.objects.get(id=pk)
        comments = Comment.objects.filter(incident=incident)
        
        return render(request, 'incident/view.html', {
            'incident': incident,
            'comments': comments,
            'form': form
        })
        
    else:
        return redirect('home')

def remove(request, pk):
    if request.user.is_authenticated:
        delete_it = Incident.objects.get(id=pk)
        AuditLog.objects.create(user=request.user, text=f"{request.user} removed incident {delete_it} successfully.")
        delete_it.delete()
        messages.success(request, "System removed successfully")
        return redirect('incidents:list')
    else:
        return redirect('home')

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')