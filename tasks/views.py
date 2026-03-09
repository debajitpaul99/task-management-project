from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm, TaskDetailModelForm, ProjectForm, ContactForm
from tasks.models import Task, TaskDetails, Project
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.utils.decorators import method_decorator
from users.views import is_admin
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail

# Create your views here.
def is_manager(user):
    return user.groups.filter(name="Manager").exists()

def is_employee(user):
    return user.groups.filter(name="Employee").exists()


@login_required
@permission_required("tasks.view_task", login_url="no-permission")
def manager_dashboard(request):
    tasks = Task.objects.select_related("taskdetails").prefetch_related("assigned_to").all()
    counts = Task.objects.aggregate(
        total_tasks = Count('id'),
        completed_tasks = Count('id', filter=Q(status = "COMPLETED")),
        pending_tasks = Count('id', filter=Q(status = "PENDING")),
        in_progress_tasks = Count('id', filter=Q(status = "IN_PROGRESS"))
    )

    # Retriving Task Data
    base_query = Task.objects.select_related("taskdetails").prefetch_related("assigned_to")
    type = request.GET.get('type')
    if type == "completed":
        tasks = base_query.filter(status = "COMPLETED")
    elif type == "pending":
        tasks = base_query.filter(status = "PENDING")
    elif type == "in_progress":
        tasks = base_query.filter(status = "IN_PROGRESS")
    elif type == "all":
        tasks = base_query.all()

    context = {
        "tasks" : tasks,
        "counts" : counts
    }
    return render(request,'dashboard/manager_dashboard.html',context)

@user_passes_test(is_employee, login_url="no-permission")
def employee_dashboard(request):
    return render(request,'dashboard/user_dashboard.html')

class CreateTask(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "tasks.add_task"
    login_url = "sign-in"

    template_name = "task_form.html"

    def get(self, request, *args, **kwargs):
        task_form = TaskModelForm()
        task_detail_form = TaskDetailModelForm()
        context = {
        "task_form": task_form,
        "task_detail_form": task_detail_form
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_details_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_details_form.is_valid():
            task = task_form.save()
            task_detail = task_details_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Added Successfully")
            return redirect("create-task")


class UpdateTask(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = "sign-in"
    permission_required = "tasks.add_task"

    model = Task
    form_class = TaskModelForm
    context_object_name = "task"
    template_name = "task_form.html"
    pk_url_kwarg = "task_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_form"] = self.get_form()
        if hasattr(self.object, "taskdetails"):
            context["task_detail_form"] = TaskDetailModelForm(instance=self.object.taskdetails)
        else:
            context["task_detail_form"] = TaskDetailModelForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)
        task_details_form = None
        if hasattr(self.object, "taskdetails"):
            task_details_form = TaskDetailModelForm(request.POST, request.FILES, instance=self.object.taskdetails)
        else:
            task_details_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_details_form.is_valid():
            task = task_form.save()
            task_detail = task_details_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Updated Successfully")
            return redirect("update-task", self.object.id)
        return redirect("update-task", self.object.id)


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("tasks.delete_task", login_url="no-permission"), name="dispatch")
class DeleteTask(DeleteView):
    model = Task
    success_url = reverse_lazy("manager-dashboard")
    pk_url_kwarg = "task_id"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Task Deleted Successfully")
        return redirect("manager-dashboard")
    

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("tasks.view_task", login_url="no-permission"), name="dispatch")
class TaskDetails(DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = "task"
    pk_url_kwarg = "task_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_status_choices"] = Task.STATUS_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get("task_status")
        task.status = selected_status
        task.save()
        return redirect("task-details", task.id)

class CreateProject(LoginRequiredMixin,PermissionRequiredMixin,View):
    login_url = "sign-in"
    permission_required = "tasks.add_project"
    template_name = "project_form.html"

    def get(self, request, *args, **kwargs):
        project_form = ProjectForm()
        context = {
        "project_form": project_form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project_form.save()
            messages.success(request, "Project Created Successfully")
            return redirect("create-project")


class UpdateProject(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = "sign-in"
    permission_required = "tasks.change_project"

    model = Project
    form_class = ProjectForm
    context_object_name = "projects"
    template_name = "project_form.html"
    pk_url_kwarg = "project_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_form"] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        project_form = ProjectForm(request.POST, instance=self.object)
        
        if project_form.is_valid():
            project_form.save()
            messages.success(request, "Project Updated Successfully")
            return redirect("project-details", self.object.id)
        return redirect("project-details", self.object.id)
    

class DeleteProject(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = "sign-in"
    permission_required = "tasks.delete_project"

    model = Project
    success_url = reverse_lazy("view-projects")
    pk_url_kwarg = "project_id"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Project Deleted Successfully")
        return redirect("view-projects")


class ProjectDetails(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = "sign-in"
    permission_required = "tasks.view_project"

    model = Project
    template_name = 'project_details.html'
    context_object_name = "projects"
    pk_url_kwarg = "project_id"

    def get_queryset(self):
        return Project.objects.annotate(total_tasks=Count("tasks"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_status_choices"] = Project.STATUS_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        project = self.get_object()
        selected_status = request.POST.get("project_status")
        project.status = selected_status
        project.save()
        return redirect("project-details", project.id)


class ViewProject(LoginRequiredMixin,ListView):
    login_url = "sign-in"

    model = Project
    context_object_name = "projects"
    template_name = "project_view.html"

def dashboard(request):
    if is_manager(request.user):
        return redirect("manager-dashboard")
    elif is_employee(request.user):
        return redirect("employee-dashboard")
    elif is_admin(request.user):
        return redirect("admin-dashboard")
    return redirect("no-permission")
    
def home_feature(request):
    return render(request, "home_feature.html")

def home_contact(request):
    return render(request, "home_contact.html")

def contact_view(request):
    contact_form = ContactForm()
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            full_name = contact_form.cleaned_data["full_name"]
            email = contact_form.cleaned_data["email"]
            message = contact_form.cleaned_data["message"]

            send_mail(
                subject=f"New contact message from {full_name}",
                message=f"From: {full_name}\n\nMessage: {message}",
                from_email=None,
                recipient_list=["debajit2003@gmail.com"]
            )

            messages.success(request, "Your message has been sent successfully")
            return redirect("home-contact")
        
    return render(request, "home_contact.html", {"contact_form":contact_form})