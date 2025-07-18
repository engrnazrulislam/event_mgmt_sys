from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re

class RegisterForm(UserCreationForm):
    class Meta:
            model = User
            fields = ['username','first_name','last_name','password1','password2','email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        # set helptext = none in all field
        # by using loop get all fields
        for fieldname in ['username','password1','password2']:
            self.fields[fieldname].help_text = None
        
# Customized Registration Forms:
class CustomRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput) # Here is not found any password field. 
    #So we use wigets which is used to unreadable password
    confirmed_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','confirmed_password','email']

    # Now we make some clean method for validation
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        errors = []
        # Condition for error checking
        if len(password1) < 8:
            # raise forms.ValidationError('Password must be 8 character long')
            errors.append('Password must be 8 character long')
         # Home work implement regular expression

        if re.search(r'[A-Z]',password1):
            errors.append('Password does not contain any capital letter')

        if re.search(r'[a-z]',password1):
            errors.append('Password does not contain small letter')

        if re.search(r'[0-9]',password1):
            errors.append('Password does not contain any number')
        
        if re.search(r'[@*#$+=]',password1):
            errors.append('Password does not contain any special character')
                
        if errors:
            raise forms.ValidationError(errors)
        
        return password1

        # if re.fullmatch(r'[A-Za-z0-9#$%@^+=]',password1):
        #         raise forms.ValidationError('Password must contain uppercase, lowercase, min 8 character')
    # non-field validataion
    def clean(self):
        clean_data = super().clean()
        password = clean_data.get('password1')
        confirmed_password = clean_data.get('confirmed_password')

        if password and confirmed_password and password != confirmed_password:
            raise forms.ValidationError('Password does not match')

        return clean_data

    # Home work email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError('Email already exists')
        
        return email
    

   


    


