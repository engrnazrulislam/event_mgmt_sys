from django import forms
from django.contrib.auth.models import User, Group, Permission
import re
from events.forms import StyleFormMixing
from django.contrib.auth.forms import AuthenticationForm

class CustomRegistrationForm(StyleFormMixing, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmed_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'confirmed_password', 'email']  # exclude password fields

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        """
        errors = []
       
        if not len(password) > 8:
            errors.append('Password must be at least 8 characters long')

        if not re.search(r'[A-Z]', password):
            errors.append('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', password):
            errors.append('Password must contain at least one lowercase letter')

        if not re.search(r'[0-9]', password):
            errors.append('Password must contain at least one digit')

        if not re.search(r'[@*#$+=]', password):
            errors.append('Password must contain at least one special character (@, *, #, $, +, =)')

        if errors:
            raise forms.ValidationError(errors)
        """
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmed_password = cleaned_data.get('confirmed_password')

        if password and confirmed_password and password != confirmed_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

class LoginForm(StyleFormMixing, AuthenticationForm):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class AssignRoleForm(StyleFormMixing, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )

class CreateGroupForm(StyleFormMixing, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset = Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )
    class Meta:
        model = Group
        fields = ['name','permissions']