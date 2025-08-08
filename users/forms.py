from django import forms
from django.contrib.auth.models import User, Group, Permission
import re
from events.forms import StyleFormMixing
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

class CustomRegistrationForm(StyleFormMixing, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmed_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  # exclude password fields

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        
        errors = []
       
        if len(password) < 8:
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


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    bio = forms.CharField(required = False, widget = forms.Textarea, label='bio')
    phone_number = forms.CharField(required=False, widget=forms.TextInput, label='Phone Number')
    profile_image = forms.ImageField(required=False, label='Profile Image')

    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile', None)
        super().__init__(*args, **kwargs)

        # Todo: Handle Error
        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['phone_number'].initial = self.userprofile.phone_number
            self.fields['profile_image'].initial = self.userprofile.profile_image
    def save(self, commit=True):
        user = super().save(commit=False)

        #save userprofile jodi thake
        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.phone_number = self.cleaned_data.get('phone_number')
            self.userprofile.profile_image = self.cleaned_data.get('profile_image')

            if commit:
                self.userprofile.save()
        if commit:
            user.save()
        
        return user

class CustomPasswordChangeForm(StyleFormMixing, PasswordChangeForm):
    pass

class CustomPasswordResetForm(StyleFormMixing, PasswordResetForm):
    pass

class CustomPasswordResetConfirmForm(StyleFormMixing, SetPasswordForm):
    pass


"""
class EditProfileForm(StyleFormMixing, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'bio', 'profile_image']
"""