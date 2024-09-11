from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from website.functions import get_ping_graph
from systems.models import System
from config.models import Settings
from .models import Incident, Comment
from .forms import CommentForm

# Create your views here.

# validated function

def incidents(request):
    if request.user.is_authenticated:
        incidents = Incident.objects.all().order_by("-id")
        paginator = Paginator(incidents, 10)
        page_number = request.GET.get("page")
        page_incidents = paginator.get_page(page_number)

        return render(request, 'incidents.html', {'incidents': page_incidents})
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
                return render(request, 'incident.html', {
                    'incident': incident,
                    'comments': comments, 
                    'form': form,    
                })
            else:
                form = CommentForm()

        incident = Incident.objects.get(id=pk)
        comments = Comment.objects.filter(incident=incident)
        
        return render(request, 'incident.html', {
            'incident': incident,
            'comments': comments,
            'form': form
        })
        
    else:
        return redirect('home')

def remove(request, pk):
    if request.user.is_authenticated:
        delete_it = Incident.objects.get(id=pk)
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