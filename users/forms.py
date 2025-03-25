from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import Group,Permission
from django.contrib.auth import get_user_model
from cloudinary.forms import CloudinaryFileField
User = get_user_model()


class User_RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

    def __init__(self, *args, **kwargs):
        super(User_RegistrationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None
            self.fields[field_name].required = True
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different email.")
        return email

class LoginForm(AuthenticationForm):  
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class CustomPasswordChangeForm( PasswordChangeForm):
    pass


class CustomPasswordResetForm( PasswordResetForm):
    pass


class CustomPasswordResetConfirmForm( SetPasswordForm):
    pass


class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role"
    )

class createGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Group
        fields = ['name', 'permissions']

class User_EditForm(forms.ModelForm):
    profile_picture = CloudinaryFileField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'profile_picture', 'bio']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone': 'Phone Number',
            'profile_picture': 'Profile Picture',
            'bio': 'Bio'
        }
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={
                'style': 'border: 2px solid #070; border-radius: 5px; padding: 5px; cursor: pointer; margin-top:10px ;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(User_EditForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = False
        # Ensure 'phone' is not required
        self.fields['phone'].required = False
        self.fields['phone'].widget.attrs.update({'placeholder': 'Optional'})

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # If the phone field is empty, store the value as None (null in the database)
        if not phone:
            return 'Not Provided'
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # If the email has changed and is already used by another user, raise an error
        if email != self.instance.email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different email.")
        return email
