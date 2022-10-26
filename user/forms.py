from django import forms
from django.contrib.auth.models import User,Group
from django.forms.widgets import TextInput,Select,EmailInput,PasswordInput,FileInput,DateInput

from student.models import StudentMark, Subjects
from user.models import UserProfile

class AdminRegistrationForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['name','phone','email','password','image','date_of_birth']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Name'}),
            'phone': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Phone'}),
            'date_of_birth': DateInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Date of Birth'}),
            'email': EmailInput(attrs={'class': 'required form-control text-area','rows':'2','placeholder' : 'Enter Email'}),
            'password': PasswordInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Password'}),
            'image': FileInput(),
        }

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','password']

        widgets = {
            'username': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Name'}),
            'password': PasswordInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Password'}),
        }


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subjects
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Name'}),
        }


class StudentMarkForm(forms.ModelForm):

    class Meta:
        model = StudentMark
        fields = ['subject','mark']

        widgets = {
            'subject': Select(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Name'}),
            'mark': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Name'}),
        }