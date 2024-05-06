from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Log, Dataset
from .forms import SignUpForm, AddDatasetForm, AddModelForm
from .ml_models import create_model

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


# datasets

def view_datasets(request):
    if request.user.is_authenticated:
        datasets = Dataset.objects.all()
        return render(request, 'datasets.html', {'datasets': datasets})
    else:
        return redirect('home')


def add_dataset(request):
    if request.user.is_authenticated:
        form = AddDatasetForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Dataset added successfully")
                return redirect('datasets')
        else:
            return render(request, 'add_dataset.html', {'form':form})
    else:
        return redirect('home')


def delete_dataset(request, pk):
    if request.user.is_authenticated:
        delete_it = Dataset.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Dataset deleted successfully!")
        return redirect('datasets')
    else:
        return redirect('home')


def update_dataset(request, pk):
    if request.user.is_authenticated:
        update_it = Dataset.objects.get(id=pk)
        form = AddDatasetForm(request.POST or None, instance=update_it)
        if form.is_valid():
            form.save()
            messages.success(request, "Dataset updated successfully")
            return redirect('datasets')
        else:
            return render(request, 'update_dataset.html', {'form':form})
    else:
        return redirect('home')


def view_dataset(request, pk):
    if request.user.is_authenticated:
        dataset = Dataset.objects.get(id=pk)
        dataset_data = dataset.get_dataset()
        data = dataset_data['data']
        target = dataset_data['target']

        data_with_target = []
        for log, label in zip(data, target):
            log_with_label = {'label': label, 'log': log}
            data_with_target.append(log_with_label)

        return render(request, 'dataset.html', {'dataset': dataset, 'data': data_with_target})
        pass
    else:
        return redirect('home')


# models

def view_models(request):
    if request.user.is_authenticated:
        return render(request, 'models.html')
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