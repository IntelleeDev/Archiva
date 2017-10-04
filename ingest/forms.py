from django import forms
from django.forms import ModelForm

class SignUpForm(forms.Form):   
    firstname = forms.CharField(max_length=25)
    lastname = forms.CharField(max_length=25)
    email = forms.EmailField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    cpassword = forms.CharField(min_length=8, widget=forms.PasswordInput)
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=60)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)    
    
    
class UploadForm(forms.Form):
    title = forms.CharField(max_length=25)
    content = forms.FileField()
    tags = forms.CharField()
    desc = forms.CharField()

class RepositoryForm(forms.Form):
    name =  forms.CharField(max_length=40)