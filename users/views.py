from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterForm, CustomRegistrationForm

# Create your views here.
def sign_up(request):
    if request.method == 'GET': 
        form = CustomRegistrationForm()
    elif request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'registration/registration.html',{'form':form})

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html')

    # logout implementation
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign_in')