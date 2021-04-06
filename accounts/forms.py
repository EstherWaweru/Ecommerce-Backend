from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
class SignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=('email','first_name','last_name','password1','password2')
class LoginForm(forms.Form):
    email=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    remember_me=forms.BooleanField(required=False)

