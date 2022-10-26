import datetime
import json

from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from main.functions import generate_form_errors, get_auto_id
from student.forms import StudentRegistrationForm
from main.decorators import role_required
from student.models import StudentDetails,StudentMark

# Create your views here.
@login_required
@role_required(['student'])
def index(request):
    instance = StudentDetails.objects.get(user=request.user, is_deleted=False)
    marks = StudentMark.objects.filter(student=instance, is_deleted=False)

    context = {
        'instance': instance,
        'marks': marks,
        'page_name' : 'Student Details',
        'page_title' : 'Student Details',
        "is_student" : True,
        'is_need_select2' : True,
    }
    return render(request, "student/index.html",context)


def student_registration(request):

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST,request.FILES)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user_data = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    is_active=True,
                )

            if Group.objects.filter(name="student").exists():
                group = Group.objects.get(name="student")
            else:
                group = Group.objects.create(name="student")

            user_data.groups.add(group)

            data = form.save(commit=False)
            data.auto_id = get_auto_id(StudentDetails)
            data.creator = user_data
            data.date_updated = datetime.datetime.today()
            data.updater = user_data
            data.user = user_data
            data.save()

            user = authenticate(username=email, password=password)

            if user is not None:
                login(request,user)

                # print('true')

            response_data = {
                    "status": 'true',
                    "redirect": True,
                    "url": reverse('student:student_dashboard'),
            }

        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = StudentRegistrationForm()

        context = {
            'form': form,
            'page_name' : 'Student Registration',
            'page_title' : 'Student Registration',
            'url' : reverse('student:student_dashboard'),
            "is_student" : True,
            'is_need_select2' : True,
        }

        return render(request, 'registration/registration.html',context)


@login_required
@role_required(['student'])
def edit_student(request,pk):
    """
    edit operation of student
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(StudentDetails, pk=pk)

    message = ''
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST,instance=instance)

        if form.is_valid():

            #create student
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "StudentDetails created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('student:student_dashboard')
            }

        else:
            message = generate_form_errors(form ,formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = StudentRegistrationForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Create StudentDetails',
            'page_title' : 'Create StudentDetails',
            'url' : reverse('student:student_dashboard'),
            "is_student" : True,
            'is_need_select2' : True,
        }

        return render(request, 'admin_panel/create/create.html',context)





