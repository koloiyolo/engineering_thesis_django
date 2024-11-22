from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from systems.models import System
from config.models import Settings
from .models import Incident, Comment
from .forms import CommentForm

# Create your views here.

# validated function

def incidents(request):
    if request.user.is_authenticated:
        incidents = Incident.objects.all().order_by("-id")
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(incidents, items_per_page)
        page_number = request.GET.get("page")
        page_incidents = paginator.get_page(page_number)

        return render(request, 'incident/list.html', {'incidents': page_incidents})
    else:
        return redirect('home')

def tag_incidents(request, tag):
    if request.user.is_authenticated:
        query = request.GET.get('q', '')
        incidents = Incident.objects.filter(tag=tag, ip__icontains=query).order_by("-id")
        if not incidents.exists():
            messages.warning(request, f"Label '{tag}' is empty!")
            return redirect('incidents:list')
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(incidents, items_per_page)
        page_number = request.GET.get("page")
        page_incidents = paginator.get_page(page_number)

        return render(request, 'incident/list.html', {'incidents': page_incidents})
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
                return render(request, 'incident/view.html', {
                    'incident': incident,
                    'comments': comments, 
                    'form': form,    
                })
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