from django.shortcuts import render, redirect
from users.forms import User_RegistrationForm
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from users.forms import AssignRoleForm, createGroupForm
from django.views.decorators.http import require_GET
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
import time


def is_admin(user):
   return user.groups.filter(name='Admin').exists()

def profile(request):
  return render(request,'profile.html')

class EditProfileView(LoginRequiredMixin,UpdateView):
    login_url = "sign-in"
    model = User
    from_class = 'EditProfileForm'
    context_object_name ='form'
    template_name ='accounts/update_profile.html'
    
    def get_object(self):
       return super().request.user
     
    def form_valid(self,form):
      form.save()
      return redirect("Profile")


def sign_up(request):
  form = User_RegistrationForm()
  if request.method == "POST":
    form = User_RegistrationForm(request.POST)
    if form.is_valid():
      user= form.save(commit=False)
      user.set_password(form.cleaned_data.get('password1'))
      user.is_active = False
      user.save()
      messages.success(request, 'A confirmation email has been sent to your email address. Please click on the link to activate your account.')
      return redirect('sign_in')
  return render(request, 'registration/registration.html', {'form': form})


def sign_in(request):
  form = AuthenticationForm()
  if request.method=='POST':
    form = AuthenticationForm(request,data=request.POST)
    if form.is_valid():
      user = form.get_user()
      if user is not None and user.is_authenticated:
        login(request,user)
        messages.success(request, 'Login Sucessfully')
        time.sleep(0.5)  
        return redirect('home')
      else:
        messages.error(request, 'Please Enter Correct Username and Password')
    else:
        messages.error(request, 'Please Enter Correct Username and Password')
  return render (request, 'registration/login.html',{'form':form})


@login_required
def sign_out(request):
  logout(request)
  messages.success(request,"logout Sucessfully")
  return redirect('sign_in')


@require_GET
def activate_user(request, user_id, token):
  try:
    user = User.objects.get(pk=user_id)
    if default_token_generator.check_token(user, token):
      user.is_active = True
      user.save()
      messages.success(request, "Your account has been activated successfully. You can now login.")
      return redirect('sign_in')
    else:
      messages.error(request, "Invalid activation link.")
      return redirect('sign_in')
  except User.DoesNotExist:
    messages.error(request, "Invalid user.")
    return redirect('login')

@login_required
@user_passes_test(is_admin, login_url='sign_in')
def admin_dashboard(request):
    users = User.objects.all()
    
    return render(request, 'admin/admin_dashboard.html',{'users':users })

@login_required
@user_passes_test(is_admin, login_url='sign_in')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f'{user.username} role has been updated to {role.name}')
            return redirect('admin_dashboard')   
    return render(request, 'admin/assign_role.html', {'form': form, 'user': user})

@login_required
@user_passes_test(is_admin, login_url='sign_in')
def create_group(request):
    form = createGroupForm()
    if request.method== 'POST':
       form = createGroupForm(request.POST)
       if form.is_valid():
          group = form.save()
          messages.success(request, f'{group.name} has been created successfully') 
          return redirect('group_list')   
    return render(request, 'admin/create_group.html', {'form': form})

def update_group(request, group_id):
    group = Group.objects.get(id=group_id)
    form = createGroupForm(instance=group)
    if request.method == 'POST':
        form = createGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, f'{group.name} has been updated successfully')
            return redirect('group_list')
    return render(request, 'admin/create_group.html', {'form': form, 'group': group})


@login_required
@user_passes_test(is_admin, login_url='sign_in')
def group_list(request):
    groups = Group.objects.only('id', 'name').prefetch_related('permissions')
    return render(request, 'admin/group_list.html', {'groups': groups})
