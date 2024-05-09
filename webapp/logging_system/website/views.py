from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Log, ClassifiedData
from .forms import SignUpForm, ClassifyForm

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


# ML Models

def view_models(request):
    if request.user.is_authenticated:
        models = MlModel.objects.all()
        return render(request, 'models.html', {'models': models})
    else:
        return redirect('home')

def classify(request):
    if request.user.is_authenticated:
        form = ClassifyForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Classification completed successfully")
                pk = ClassifiedData.objects.order_by('-id').first().id
                return redirect('classified_data', pk = pk)
        else:
            return render(request, 'classify.html', {'form': form})
        return render(request, 'classify.html', {'form': form})
    else:
        return redirect('home')

def classified_data(request, pk):
    if request.user.is_authenticated:
        classified_data = ClassifiedData.objects.get(id=pk)

        data = classified_data.get_data()
        target = data['target']
        data = data['data']

        data_with_target = []
        for log, label in zip(data, target):
            log_with_label = {'label': label, 'log': log}
            data_with_target.append(log_with_label)
        data_with_target = sorted(data_with_target, key=lambda x: x['label'])
        return render(request, 'classified_data.html', {'classified_data': classified_data, 'data': data_with_target})
    else:
        return redirect('home')

def delete_classified_data(request, pk):
    if request.user.is_authenticated:
        delete_it = ClassifiedData.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect('ml_archive')
    else:
        messages.success(request, "Operation failed!")
        return redirect('ml_archive')

def ml_archive(request):
    if request.user.is_authenticated:
        classified_data = ClassifiedData.objects.all()
        return render(request, 'ml_archive.html', {'classified_data': classified_data})
    else:
        return redirect('home')




# validated function

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')