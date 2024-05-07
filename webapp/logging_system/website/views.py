from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Log, MlModel
from .forms import SignUpForm, AddModelForm

# Create your views here.

def home(request):
    
    logs = Log.objects.all()[:5000]

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.success(request, "Failed to log in, try again!")
            return redirect('home')

    else:
        return render(request, 'home.html', {'logs':logs})
    return render(request, 'home.html', {'logs':logs})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfuly created an account!")
            return redirect('home')
        pass
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
        
    return render(request, 'register.html', {'form': form})


# models

def view_models(request):
    if request.user.is_authenticated:
        models = MlModel.objects.all()
        return render(request, 'models.html', {'models': models})
    else:
        return redirect('home')

def add_model(request):
    if request.user.is_authenticated:
        form = AddModelForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Model added successfully")
                return redirect('models')
        else:
            return render(request, 'add_model.html', {'form':form})
        return render(request, 'add_model.html', {'dataset': dataset})
    else:
        return redirect('home')







# validated function
# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')