from django.contrib.auth.forms import UserCreationForm
from django import forms
import re
from django.contrib.auth.models import User
from tasks.forms import StyledFormMixin

class CustomRegistrationForm(forms.ModelForm):
    password = forms.CharField()
    confirm_password = forms.CharField()
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password', 'confirm_password']
    
    
    def clean_password(self):  # "clean_fieldname" method is used for accessing field error
        errors = []
        pw = self.cleaned_data.get('password')
        if len(pw) < 8:
            errors.append("Password must be in 8 characters")
        
        if not re.search(r"[A-Z]", pw):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")

        if not re.search(r"[a-z]", pw):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")

        if not re.search(r"\d", pw):
            raise forms.ValidationError("Password must contain at least one number.")

        if errors:
            raise forms.ValidationError(errors)
        
        return pw

    def clean(self): # "clean" method is used for accessing non-field error
        cleaned_data = super().clean()
        pw = cleaned_data.get("password")
        cpw = cleaned_data.get("confirm_password")

        if pw != cpw:
            raise forms.ValidationError("Password don't match")
        
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists")
        
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # hash password
        if commit:
            user.save()
        return user