from django.urls import path
from tasks.views import manager_dashboard, employee_dashboard, dashboard, home_feature, home_contact, CreateTask, UpdateTask, ViewProject, TaskDetails, DeleteTask, CreateProject, UpdateProject, DeleteProject, ProjectDetails, contact_view

urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name='manager-dashboard'),
    path('employee-dashboard/', employee_dashboard, name="employee-dashboard"),
    path('task-form/', CreateTask.as_view(), name='create-task'),
    path('view-projects/', ViewProject.as_view(), name="view-projects"),
    path('update-task/<int:task_id>/', UpdateTask.as_view(), name='update-task'),
    path('delete-task/<int:task_id>/', DeleteTask.as_view(), name='delete-task'),
    path('task-details/<int:task_id>/', TaskDetails.as_view(), name="task-details"),
    path('dashboard/', dashboard, name="dashboard"),
    path('features/', home_feature, name="home-feature"),
    path('contact/', contact_view, name="home-contact"),
    path('create-project/', CreateProject.as_view(), name="create-project"),
    path('update-project/<int:project_id>/', UpdateProject.as_view(), name="update-project"),
    path('delete-project/<int:project_id>/', DeleteProject.as_view(), name="delete-project"),
    path('project-details/<int:project_id>/', ProjectDetails.as_view(), name="project-details")
]