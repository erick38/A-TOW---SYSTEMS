from django.contrib.auth import models
from django.contrib.auth.models import AbstractUser, User
from django.http import request
from towingapp.models import Clock_in, MyUser
from django import forms
class login_form(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class addclockinform(forms.Form):
    author = forms.ModelMultipleChoiceField(
                                        queryset=(MyUser.objects.all())
                                        )
    
    STATUS_CHOICES = (
            ('clock-in', 'clock-in'),
            ('clock-out', 'clock-out'),
            )
    clock_status = forms.ChoiceField(choices=STATUS_CHOICES)

class add_AccountForm(forms.Form):
    username = forms.CharField(max_length=38)
    password = forms.CharField(widget=forms.PasswordInput)

class AddmessageForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=40)
    message = forms.CharField(widget=forms.Textarea)
