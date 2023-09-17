from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from django.views import View
from PIL import Image
import os
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages

# Create your views here.
from .models import Workcenter, Accident, MaintenanceTask, User, Profile, Role
from .forms import CreateAccidentForm, AdditionalImageFormSet, CreateTaskForm, EditTaskProgressForm, CreateWorkcenterForm

class HasRequiredRoleMixin:
    def has_required_role(self, user, required_roles):
        user_roles = user.profile.role_set.values_list('name', flat=True)
        return any(role in user_roles for role in required_roles)

def index(request):
    return render(request, 'main.html')

def workcenter_list(request):
    workcenters = Workcenter.objects.all()
    accidents = Accident.objects.all()
    sort_order = request.GET.get('sort_order', 'descendingProgress')

    if sort_order == 'descendingProgress':
        accidents = accidents.order_by('-progress', 'workcenter__name')
    elif sort_order == 'ascendingProgress':
        accidents = accidents.order_by('progress', 'workcenter__name')
    elif sort_order == 'descendingPriority':
        accidents = accidents.order_by('-priority', 'workcenter__name')
    elif sort_order == 'ascendingPriority':
        accidents = accidents.order_by('priority', 'workcenter__name')
    elif sort_order == 'ascendingStartDate':
        accidents = accidents.order_by('start_date', 'workcenter__name')
    elif sort_order == 'descendingStartDate':
        accidents = accidents.order_by('-start_date', 'workcenter__name')
    elif sort_order == 'ascendingDueDate':
        accidents = accidents.order_by('due_date', 'workcenter__name')
    elif sort_order == 'descendingDueDate':
        accidents = accidents.order_by('-due_date', 'workcenter__name')


    context = {'workcenters': workcenters, 'accidents': accidents, 'sort_order': sort_order}
    return render(request, 'maintenance/workcenter_list.html', context)


def workcenter_detail(request, pk):
    workcenter = Workcenter.objects.get(id=pk)
    workcenters = Workcenter.objects.all()
    accidents = Accident.objects.filter(workcenter=workcenter)
    sort_order = request.GET.get('sort_order', 'descendingProgress' )

    if sort_order == 'descendingProgress':
        accidents = accidents.order_by('-progress')
    elif sort_order == 'ascendingProgress':
        accidents = accidents.order_by('progress')
    elif sort_order == 'descendingPriority':
        accidents = accidents.order_by('-priority')
    elif sort_order == 'ascendingPriority':
        accidents = accidents.order_by('priority')
    elif sort_order == 'ascendingStartDate':
        accidents = accidents.order_by('start_date')
    elif sort_order == 'descendingStartDate':
        accidents = accidents.order_by('-start_date')
    elif sort_order == 'ascendingDueDate':
        accidents = accidents.order_by('due_date')
    elif sort_order == 'descendingDueDate':
        accidents = accidents.order_by('-due_date')

    current_date = datetime.now().date()

    for accident in accidents:
        days_since_creation = (current_date - accident.start_date.date()).days
        accident.days_since_creation = days_since_creation
        days_to_date = (accident.due_date.date() - current_date).days
        accident.days_to_date = days_to_date
    context = {'workcenter': workcenter,
               'workcenters': workcenters,
               'accidents': accidents,
               'sort_order': sort_order,
               }

    return render(request, 'maintenance/workcenter_detail.html', context)

def accident_detail(request, pk):
    accident = Accident.objects.get(id=pk)
    additional_images = Accident.AdditionalImage.objects.all()
    current_accident = get_object_or_404(Accident, id=pk)
    tasks = MaintenanceTask.objects.filter(accident=accident)


    context = {"accident": accident,
               'additional_images': additional_images,
               'current_accident': current_accident,
               'tasks': tasks}
    return render(request, 'maintenance/accident_detail.html', context)

@login_required(login_url="login")
def create_accident(request):
    if request.method == 'POST':
        form = CreateAccidentForm(request.POST, request.FILES)
        formset = AdditionalImageFormSet(request.POST, request.FILES, instance=form.instance)
        if form.is_valid() and formset.is_valid():

            accident = form.save(commit=False)
            accident.created_by = request.user
            accident.save()
            form.additional_images_formset.save()
            return redirect('workcenter_list')
    else:
        form = CreateAccidentForm()
        formset = AdditionalImageFormSet(instance=Accident())

    return render(request, 'maintenance/create_accident.html', {'form': form, 'formset': formset})

# def edit_accident(request, pk):
#     accident = get_object_or_404(Accident, id=pk)
#
#     if request.method == 'POST':
#         form = CreateAccidentForm(request.POST, request.FILES, instance=accident)
#         formset = AdditionalImageFormSet(request.POST, request.FILES, instance=accident)
#
#         if form.is_valid() and formset.is_valid():
#             form.save()
#             # formset.save()
#             form.additional_images_formset.save()
#             return redirect(
#                 'workcenter_list')
#     else:
#         form = CreateAccidentForm(instance=accident)
#         formset = AdditionalImageFormSet(instance=accident)
#
#     return render(request, 'maintenance/create_accident.html', {'form': form, 'formset': formset})

class EditAccident(LoginRequiredMixin, HasRequiredRoleMixin, View):
    template_name = 'maintenance/create_accident.html'
    model = Accident
    form_class = CreateAccidentForm
    login_url = "login"
    def get(self, request, uuid):
        accident = Accident.objects.get(id=uuid)
        required_roles = ["MaintenanceManager", "MaintenanceOperator"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission", pk=accident.id)

        form = self.form_class(instance=accident)  # Předvyplníme form údaji z konkrétního úkolu
        context = {
            'form': form,
            'accident': accident,
        }
        return render(request, self.template_name, context)

    # def post(self, request, uuid):
    #     accident = Accident.objects.get(id=uuid)
    #     required_roles = ["MaintenanceManager"]
    #
    #     if not self.has_required_role(request.user, required_roles):
    #         return redirect("no_permission", pk=accident.id)
    #
    #     form = self.form_class(request.POST, instance=accident)
    #
    #     if form.is_valid():
    #         form.save()
    #         return redirect('accident_detail', pk=accident.id)
    #     context = {'form': form, 'accident': accident}
    #     return render(request, self.template_name, context)

    def post(self, request, uuid):
        accident = Accident.objects.get(id=uuid)
        required_roles = ["MaintenanceManager"]


        if self.has_required_role(request.user, required_roles) or request.user == accident.created_by:
            form = self.form_class(request.POST, instance=accident)

            if form.is_valid():
                form.save()
                return redirect('accident_detail', pk=accident.id)
        else:
            return redirect("no_permission", pk=accident.id)

        context = {'form': form, 'accident': accident}
        return render(request, self.template_name, context)

class DeleteAccident(LoginRequiredMixin, HasRequiredRoleMixin,View):
    template_name = 'maintenance/delete_accident.html'
    model = Accident
    login_url = "login"

    def get(self, request, pk):
        accident = Accident.objects.get(id=pk)
        required_roles = ["MaintenanceManager", "MaintenanceOperator"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission", pk=accident.id)

        context = {
            'accident': accident,
        }

        return render(request, 'maintenance/delete_accident.html', context)

    def post(self, request, pk):
        accident = Accident.objects.get(id=pk)
        required_roles = ["MaintenanceManager"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission", pk=accident.id)
        if request.method == 'POST':
            accident.delete()

            return redirect('workcenter_list')


class CreateTask(LoginRequiredMixin, HasRequiredRoleMixin, View):
    login_url = "login"
    template_name = 'maintenance/create_task.html'
    model = MaintenanceTask
    form_class = CreateTaskForm

    def get(self, request, uuid):
        required_roles = ["MaintenanceManager"]
        accident = Accident.objects.get(id=uuid)
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission", pk=accident.id)

        initial_data = {'accident': accident,
                        'created_by': request.user}
        form = self.form_class(initial=initial_data)

        context = {
            'form': form,
            'accident': accident,
        }
        return render(request, self.template_name, context)

    def post(self, request, uuid):
        required_roles = ["MaintenanceManager"]
        accident = Accident.objects.get(id=uuid)
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission", pk=accident.id)

        form = self.form_class(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.accident = accident
            task.created_by = request.user
            task.save()
            return redirect('accident_detail', pk=uuid)
        context = {'form': form, 'accident': accident}
        return render(request, self.template_name, context)

class EditTask(LoginRequiredMixin, HasRequiredRoleMixin, View):
    login_url = "login"
    template_name = 'maintenance/create_task.html'
    form_class = CreateTaskForm

    def get(self, request, uuid):
        required_roles = ["MaintenanceManager", "MaintenanceOperator"]
        task = MaintenanceTask.objects.get(id=uuid)
        accident = task.accident
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission", pk=accident.id)

        form = self.form_class(instance=task)
        context = {
            'form': form,
            'accident': accident,
        }
        return render(request, self.template_name, context)

    def post(self, request, uuid):
        required_roles = ["MaintenanceManager"]
        task = MaintenanceTask.objects.get(id=uuid)
        accident = task.accident
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission", pk=accident.id)

        form = self.form_class(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('accident_detail', pk=accident.id)
        context = {'form': form, 'accident': accident}
        return render(request, self.template_name, context)


class DeleteTask(LoginRequiredMixin, HasRequiredRoleMixin, View):
    login_url = "login"
    template_name = 'maintenance/delete_task.html'
    model = MaintenanceTask


    def get(self, request, uuid):
        task = MaintenanceTask.objects.get(id=uuid)
        accident = task.accident
        required_roles = ["MaintenanceManager", "MaintenanceOperator"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission", pk=accident.id)


        context = {'task': task, 'accident': accident}

        return render(request, 'maintenance/delete_task.html', context)

    def post(self, request, uuid):
        task = MaintenanceTask.objects.get(id=uuid)
        accident = task.accident
        required_roles = ["MaintenanceManager"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission", pk=accident.id)

        if request.method == 'POST':
            task.delete()

            return redirect('accident_detail', pk=accident.id)

def no_permission(request, pk):
    accident = Accident.objects.get(id=pk)


    context = {
        'accident': accident,
    }
    return render(request, 'maintenance/no_permission.html', context)

def no_permission_workcenter(request, pk):

    workcenter = Workcenter.objects.get(id=pk)

    context = {
        'workcenter': workcenter,
    }
    return render(request, 'maintenance/no_permission_workcenter.html', context)

class EditTaskProgress(LoginRequiredMixin, HasRequiredRoleMixin, View):
    login_url = "login"
    template_name = 'maintenance/create_task.html'
    form_class = EditTaskProgressForm

    def get(self, request, uuid):
        required_roles = ["MaintenanceManager", "MaintenanceOperator"]
        task = MaintenanceTask.objects.get(id=uuid)
        accident = task.accident
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission", pk=accident.id)

        form = self.form_class(instance=task)  # Předvyplníme form údaji z konkrétního úkolu
        context = {
            'form': form,
            'accident': accident,
        }
        return render(request, self.template_name, context)

    def post(self, request, uuid):
        required_roles = ["MaintenanceManager", "MaintenanceOperator"]
        task = MaintenanceTask.objects.get(id=uuid)
        accident = task.accident
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission", pk=accident.id)

        form = self.form_class(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("user_account")
        context = {'form': form, 'accident': accident}
        return render(request, self.template_name, context)

class CreateWorkcenter(LoginRequiredMixin, HasRequiredRoleMixin, View):
    login_url = "login"
    template_name = 'maintenance/create_workcenter.html'
    model = Workcenter
    form_class = CreateWorkcenterForm

    def get(self, request):
        required_roles = ["MaintenanceManager", "MaintenanceOperator"]

        if not self.has_required_role(request.user, required_roles):
            return redirect("workcenter_list")

        form = self.form_class() # Předvyplníme form pro konkrétní accident
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        required_roles = ["MaintenanceManager", "MaintenanceOperator"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("workcenter_list")

        form = self.form_class(request.POST)

        if form.is_valid():
            workcenter = form.save(commit=False)
            workcenter.save()
            return redirect("workcenter_list")
        context = {'form': form}
        return render(request, self.template_name, context)

class DeleteWorkcenter(LoginRequiredMixin, HasRequiredRoleMixin, View):
    login_url = "login"
    template_name = 'maintenance/delete_workcenter.html'
    model = Workcenter

    def get(self, request, pk):
        workcenter = Workcenter.objects.get(id=pk)
        required_roles = ["MaintenanceManager", "MaintenanceOperator"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission_workcenter", pk=workcenter.id)


        context = {'workcenter': workcenter}

        return render(request, 'maintenance/delete_workcenter.html', context)

    def post(self, request, pk):
        workcenter = Workcenter.objects.get(id=pk)

        required_roles = ["MaintenanceManager"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("no_permission_workcenter", pk=workcenter.id)

        if request.method == 'POST':
            workcenter.delete()

            return redirect('workcenter_list')