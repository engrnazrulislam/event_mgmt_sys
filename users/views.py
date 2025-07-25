from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from users.forms import CustomRegistrationForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Prefetch

# Create your views here.
def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "User is created successfully.")
            return redirect('sign_in')
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
@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign_in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')


#User passes_test function
def is_admin(user):
    return user.groups.filter(name='admin').exists()

@user_passes_test(is_admin, login_url='no_permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No group assigned'

    return render(request,'admin/dashboard.html',{'users':users})

@user_passes_test(is_admin, login_url='no_permission')
def assigned_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect('admin_dashboard')

    return render(request, 'admin/assigned_role.html', {"form": form})

@user_passes_test(is_admin, login_url='no_permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group=form.save()
            messages.success(request,f"Group {group.name} has been created Successfully!!")
            return redirect('create_group')
    return render(request,'admin/create_group.html',{'form':form})        

@user_passes_test(is_admin, login_url='no_permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request,'admin/group_list.html',{'groups':groups})