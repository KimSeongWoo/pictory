from django.shortcuts import render
from .forms import  ProfileStateForm, ProfileModifyForm
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.

#-----------------------profile------------------------    

def profile(request):
    return render(request,'profile.html')

def edit_profile(request):
    return render(request,'profileedit.html')
