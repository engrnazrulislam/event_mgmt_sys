from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterForm

# Create your views here.
def sign_up(request):
    if request.method == 'GET': 
        form = RegisterForm()
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'registration/registration.html',{'form':form})