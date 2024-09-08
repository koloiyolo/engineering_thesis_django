from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from website.functions import get_ping_graph
from systems.models import System
from config.models import Settings
# Create your views here.

# validated function

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')