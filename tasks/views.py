from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm, TaskDetailModelForm, EmployeeForm
from tasks.models import Employee, Task, TaskDetails, Project
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages

# Create your views here.
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

def user_dashboard(request):
    return render(request,'dashboard/user_dashboard.html')

def test(request):
    context = {
        "name": ['Debajit','Shri','Aury']
    }
    return render(request,'test.html',context)

def task_form(request):
    task_form = TaskModelForm() # This form is for GET method
    task_details_form = TaskDetailModelForm()
    if request.method == "POST":
        task_form = TaskModelForm(request.POST) # This form is for POST method
        task_details_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_details_form.is_valid():
            task = task_form.save()
            task_detail = task_details_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Added Successfully")
            return redirect("create-task")
    context = {
        "task_form": task_form,
        "task_details_form": task_details_form
    }
    return render(request, "task_form.html",context)

def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task) # This form is for GET method
    task_details_form = TaskDetailModelForm(instance=task.taskdetails)
    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task) # This form is for POST method
        task_details_form = TaskDetailModelForm(request.POST, instance=task.taskdetails)
        if task_form.is_valid() and task_details_form.is_valid():
            task = task_form.save()
            task_detail = task_details_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Updated Successfully")
            return redirect("update-task", id)
    context = {
        "task_form": task_form,
        "task_details_form": task_details_form
    }
    return render(request, "task_form.html",context)

def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task Deleted Successfully")
        return redirect("manager-dashboard")
    return redirect("manager-dashboard")

def view_tasks(request):
    task_count = Project.objects.annotate(num_of_task=Count("task")).order_by("num_of_task")
    return render(request, "task_view.html", {"tasks": task_count})

def add_employee(request):
    emp_form = EmployeeForm()
    if request.method == "POST":
        emp_form = EmployeeForm(request.POST)
        if emp_form.is_valid():
            emp_form.save()
            return redirect("add-emp")
        
    context = {"emp_form" : emp_form}
    return render(request, "emp_form.html", context)

