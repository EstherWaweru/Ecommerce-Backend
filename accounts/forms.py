from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=('email','first_name','last_name','password1','password2')
