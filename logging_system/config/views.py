from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render

from logging_system.audit_log.models import AuditLog

from .forms import SettingsPage
from .models import Settings


# Create your views here.
@staff_member_required(login_url="/accounts/login/")
def settings(request):
    settings = Settings.load()
    form = SettingsPage(request.POST or None, instance=settings)
    if form.is_valid():
        form.save()
        AuditLog.objects.create(
            user=request.user, message=f"User {request.user} updated settings."
        )
        messages.success(request, "Settings updated successfully")
        return redirect("home")
    else:
        return render(request, "misc/settings.html", {"form": form})


@staff_member_required(login_url="/accounts/login/")
def reset(request):
    settings = Settings.load()
    settings.delete()

    AuditLog.objects.create(
        user=request.user,
        message=f"User {request.user} restored default configuration.",
    )
    messages.success(request, "Configuration restored")
    return redirect("config:settings")


@staff_member_required(login_url="/accounts/login/")
def reset_ml(request):
    settings = Settings.load()

    settings.s1_vectorizer = 1
    settings.s1_vectorizer_parameters = None
    settings.s1_clusterer = 1
    settings.s1_clusterer_parameters = None
    settings.s2_vectorizer = 0
    settings.s2_vectorizer_parameters = None
    settings.s2_clusterer = 3
    settings.s2_clusterer_parameters = None
    settings.on_model_change_reset = False
    settings.ml_anomaly_cluster = 0
    settings.ml_train = 2000
    settings.ml_train_interval = 3
    settings.ml_cluster = 10000
    settings.ml_cluster_interval = 3

    settings.save()
    AuditLog.objects.create(
        user=request.user,
        message=f"User {request.user} restored default ml configuration.",
    )
    messages.success(request, "ML configuration restored")
    return redirect("config:settings")
