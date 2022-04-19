# for userCreation
from django.contrib.auth.forms import UserCreationForm
from django import forms 


# default django user model
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            # visible.field.widget.attrs['id']="form3Example4cd"
