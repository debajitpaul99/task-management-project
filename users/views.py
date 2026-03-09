from users.forms import CustomRegistrationForm, AssignRoleForm, CreateGroupForm, EditProfileForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

# Create your views here.
def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def sign_up(request):
    form = CustomRegistrationForm()

    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return render(request, "registration/check_email.html")
    return render(request, "registration/sign_up.html", {"form" : form})

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been successfully activated")
            return redirect('sign-in')
        else:
            return HttpResponse("Invalid ID or Token")
    
    except User.DoesNotExist:
        return HttpResponse("User Not Found")

@method_decorator(login_required, name="dispatch")
@method_decorator((user_passes_test(is_admin, login_url="no-permission")), name="dispatch")
class DeleteUser(DeleteView):
    model = User
    success_url = reverse_lazy("admin-dashboard")
    pk_url_kwarg = "user_id"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, f"User {self.object.username} Removed Successfully")
        return redirect("admin-dashboard")

class CustomLogin(LoginView):
    template_name = "registration/sign_in.html"

    def get_success_url(self):        
        next_url = self.request.GET.get("next")
        return next_url if next_url else super().get_success_url()
    
    def form_valid(self, form):
        messages.success(self.request, "Login Successful")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Incorrect username or password")
        return super().form_invalid(form)
    

class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = "sign-in"
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["username"] = user.username
        context["email"] = user.email
        context["full_name"] = user.get_full_name()
        context["date_joined"] = user.date_joined
        context["last_login"] = user.last_login
        context["bio"] = user.bio
        context["profile_img"] = user.profile_image

        return context
    
class PasswordReset(PasswordResetView):
    template_name = "registration/password_reset.html"
    success_url = reverse_lazy("password-reset")
    html_email_template_name = "registration/password_reset_email_template.html"
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context

    def form_valid(self, form):
        messages.success(self.request, "A reset email sent. Please check your mail")
        return super().form_valid(form)
    
    
class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirmation.html"
    success_url = reverse_lazy("sign-in")

    def form_valid(self, form):
        messages.success(self.request, "Your password has been updated successfully")
        return super().form_valid(form)
    
@user_passes_test(is_admin, login_url="no-permission")
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, "admin/admin_dashboard.html", {"users":users})

@user_passes_test(is_admin, login_url="no-permission")
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    assign_role_form = AssignRoleForm()

    if request.method == "POST":
        assign_role_form = AssignRoleForm(request.POST)
        if assign_role_form.is_valid():
            role = assign_role_form.cleaned_data.get('role')
            user.groups.clear() #clear previous role
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the role {role}")
            return redirect("admin-dashboard")
        
    return render(request, "admin/assign_user.html", {"form":assign_role_form})

@user_passes_test(is_admin, login_url="no-permission")
def create_group(request):
    group_form = CreateGroupForm()

    if request.method == "POST":
        group_form = CreateGroupForm(request.POST)
        if group_form.is_valid():
            group = group_form.save()
            messages.success(request, f"Group {group} has been created")
            return redirect("create-group")
    
    return render(request, "admin/create_group.html", {"group_form":group_form})

@user_passes_test(is_admin, login_url="no-permission")
def show_groups(request):
    groups = Group.objects.prefetch_related("permissions").all()
    return render(request, "admin/show_groups.html", {"groups":groups})


@method_decorator(login_required, name="dispatch")
class EditUserProfile(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = "accounts/edit_profile.html"
    context_object_name = "form"
    
    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect("user-profile")
