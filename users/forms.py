from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re
from events.forms import StyleFormMixing

# Customized Registration Forms:
class CustomRegistrationForm(StyleFormMixing,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput) # Here is not found any password field. 
    #So we use wigets which is used to unreadable password
    confirmed_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password','confirmed_password','email']

    # Now we make some clean method for validation
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        errors = []
        # Condition for error checking
        if len(password) < 8:
            # raise forms.ValidationError('Password must be 8 character long')
            errors.append('Password must be 8 character long')
         # Home work implement regular expression

        if re.search(r'[A-Z]',password):
            errors.append('Password does not contain any capital letter')

        if re.search(r'[a-z]',password):
            errors.append('Password does not contain small letter')

        if re.search(r'[0-9]',password):
            errors.append('Password does not contain any number')
        
        if re.search(r'[@*#$+=]',password):
            errors.append('Password does not contain any special character')
                
        if errors:
            raise forms.ValidationError(errors)
        
        return password
    
    # non-field validataion
    def clean(self):
        clean_data = super().clean()
        password = clean_data.get('password')
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
    

   


    


