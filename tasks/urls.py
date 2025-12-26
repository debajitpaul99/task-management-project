from django.urls import path
from tasks.views import manager_dashboard, user_dashboard, test, task_form, view_tasks, update_task, delete_task, add_employee

urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name='manager-dashboard'),
    path('user-dashboard/', user_dashboard),
    path('test/', test),
    path('task-form/', task_form, name='create-task'),
    path('view-tasks/', view_tasks),
    path('update-task/<int:id>/', update_task, name='update-task'),
    path('delete-task/<int:id>/', delete_task, name='delete-task'),
    path('add-employee', add_employee, name="add-emp")
]