# for userCreation
from django.contrib.auth.forms import UserCreationForm
from django import forms 


# default django user model
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
