from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from library.models import Person

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Person
        fields = ["username", "first_name", "email", "country", "password1", "password2"]
