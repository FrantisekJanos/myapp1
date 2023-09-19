from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View
from .models import Profile, Role, Workcenter
from maintenance.models import MaintenanceTask
from .forms import CustomUserCreationForm, ProfileForm
from django.db.models import F, Value
from django.db.models.functions import Concat

# Create your views here.

def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('user_account')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login_register.html')

def logout_user(request):
    logout(request)
    messages.error(request, 'User was successfully logged out')
    return redirect('login')

def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit_account')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    excluded_username = "a091124"
    profiles = Profile.objects.exclude(user__username=excluded_username).all()
    context = {'profiles': profiles}

    return render(request, 'users/profiles.html', context)

def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    # tasks = MaintenanceTask.objects.all()
    tasks = MaintenanceTask.objects.filter(owner=profile).select_related('accident', 'accident__workcenter')
    sort_order = request.GET.get('sort_order', 'descendingProgress' )
    print(tasks)
    if sort_order == 'descendingProgress':
        tasks = tasks.order_by('-progress')
    elif sort_order == 'ascendingProgress':
        tasks = tasks.order_by('progress')
    elif sort_order == 'descendingPriority':
        tasks = tasks.order_by('-accident__priority')
    elif sort_order == 'ascendingPriority':
        tasks = tasks.order_by('accident__priority')
    elif sort_order == 'ascendingStartDate':
        tasks = tasks.order_by('start_date')
    elif sort_order == 'descendingStartDate':
        tasks = tasks.order_by('-start_date')
    elif sort_order == 'ascendingDueDate':
        tasks = tasks.order_by('due_date')
    elif sort_order == 'descendingDueDate':
        tasks = tasks.order_by('-due_date')
    elif sort_order == 'ascendingWorkcenter':
        tasks = tasks.order_by('accident__workcenter__name')
    elif sort_order == 'descendingWorkcenter':
        tasks = tasks.order_by('-accident__workcenter__name')

    context = {'profile': profile, 'tasks': tasks, 'sort_order': sort_order}

    return render(request, 'users/user_profile.html', context)

@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    tasks = MaintenanceTask.objects.filter(owner=profile).select_related('accident', 'accident__workcenter')
    sort_order = request.GET.get('sort_order', 'descendingProgress' )
    print(tasks)
    if sort_order == 'descendingProgress':
        tasks = tasks.order_by('-progress')
    elif sort_order == 'ascendingProgress':
        tasks = tasks.order_by('progress')
    elif sort_order == 'descendingPriority':
        tasks = tasks.order_by('-accident__priority')
    elif sort_order == 'ascendingPriority':
        tasks = tasks.order_by('accident__priority')
    elif sort_order == 'ascendingStartDate':
        tasks = tasks.order_by('start_date')
    elif sort_order == 'descendingStartDate':
        tasks = tasks.order_by('-start_date')
    elif sort_order == 'ascendingDueDate':
        tasks = tasks.order_by('due_date')
    elif sort_order == 'descendingDueDate':
        tasks = tasks.order_by('-due_date')
    elif sort_order == 'ascendingWorkcenter':
        tasks = tasks.order_by('accident__workcenter__name')
    elif sort_order == 'descendingWorkcenter':
        tasks = tasks.order_by('-accident__workcenter__name')
    context = {'profile': profile, 'tasks': tasks, 'sort_order': sort_order}


    return render(request, 'users/user_account.html', context)

@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('user_account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)