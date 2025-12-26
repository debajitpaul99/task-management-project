from django import forms
from tasks.models import Task, TaskDetails, Employee

class StyledFormMixin:
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.apply_styled_widgets()

    default_classes = "border-2 border-gray-100 w-1/2 rounded-md gap-4"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder' : f"Enter {(field.label or field_name).lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder' : f"Enter {(field.label or field_name).lower()}"
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : "border-2 border-gray-100 rounded-md"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : "space-y-2"
                })
            
# Django model form
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title","description","due_date","assigned_to"]
        widgets = {
            'due_date' : forms.SelectDateWidget,
            'assigned_to' : forms.CheckboxSelectMultiple
        }

class TaskDetailModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetails
        fields = ['priority', 'notes']

class EmployeeForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email']    