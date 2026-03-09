from django import forms
from tasks.models import Task, TaskDetails, Project

class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    default_classes = "mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-700"

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
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder': "Enter your email"
                })
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                })
            
# Django model form
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ["project","title","description","due_date","assigned_to"]
        widgets = {
            'due_date' : forms.SelectDateWidget,
            'assigned_to' : forms.CheckboxSelectMultiple
        }

class TaskDetailModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetails
        fields = ['priority', 'notes', 'asset']

class ProjectForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "start_date", "end_date", "status", "description"]
        widgets = {
            'start_date' : forms.SelectDateWidget,
            'end_date' : forms.SelectDateWidget
        }

class ContactForm(StyledFormMixin,forms.Form):
    full_name = forms.CharField(max_length=200, label="Full Name")
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)