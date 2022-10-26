from django import forms
from django.forms.widgets import TextInput,DateInput,EmailInput,PasswordInput,FileInput

from student.models import StudentDetails


class StudentRegistrationForm(forms.ModelForm):

    class Meta:
        model = StudentDetails
        fields = ['name','phone','email','password','image','date_of_birth','standerd']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Name'}),
            'standerd': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter standerd'}),
            'phone': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Phone'}),
            'date_of_birth': DateInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Date of Birth'}),
            'email': EmailInput(attrs={'class': 'required form-control text-area','rows':'2','placeholder' : 'Enter Email'}),
            'password': PasswordInput(attrs={'class': 'form-control h-20','placeholder' : 'Enter Password'}),
            'image': FileInput(),
        }