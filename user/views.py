import datetime
import json

from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User,Group
from django.contrib.auth import login as auth_login, authenticate, logout as logoutUser
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from student.forms import StudentRegistrationForm
from student.models import StudentDetails, StudentMark, Subjects

from user.models import UserProfile
from main.decorators import role_required
from user.forms import AdminRegistrationForm, StudentMarkForm, SubjectForm,LoginForm
from main.functions import generate_form_errors, get_auto_id

# Create your views here.
def index(request):
    return render(request, "admin_panel/index.html")

def login(request):

    if request.method == 'POST':
        # form = LoginForm(request.POST,request.FILES)
        email = request.POST['username']
        password = request.POST["password"]
        print(email,password,'iiiiiiiiii--------------------')

        if email and password:
            user = authenticate(username=email, password=password)

            if user is not None:
                auth_login(request,user)

                if User.objects.filter(id=request.user.id,groups__name="admin").exists():
                    print("admin")
                    return HttpResponseRedirect(reverse('user:admin_dashboard'))

                if User.objects.filter(id=request.user.id,groups__name="student").exists():
                    print("student")
                    return HttpResponseRedirect(reverse('student:student_dashboard'))
        else:
            message = "enter username and password"
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        context = {
            'page_name' : 'Login',
            'page_title' : 'Login',
        }

    return render(request, "registration/login.html")

def logout(request):
    logout(request)
    return render(request, "registration/login.html")


def admin_registration(request):

    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST,request.FILES)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user_data = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    is_active=True,
                )

            if Group.objects.filter(name="admin").exists():
                group = Group.objects.get(name="admin")
            else:
                group = Group.objects.create(name="admin")

            user_data.groups.add(group)

            data = form.save(commit=False)
            data.auto_id = get_auto_id(UserProfile)
            data.creator = user_data
            data.date_updated = datetime.datetime.today()
            data.updater = user_data
            data.user = user_data
            data.save()

            user = authenticate(username=email, password=password)

            if user is not None:
                login(request,user)

                # print('true')

            # response_data = {
            #         "status": 'true',
            #         "redirect": True,
            #         "url": reverse('user:admin_dashboard'),
            # }
            return HttpResponseRedirect(reverse('user:admin_dashboard'))
        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
                'is_need_select2' : True,
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = AdminRegistrationForm()

        context = {
            'form': form,
            'page_name' : 'Admin Login',
            'page_title' : 'Admin Login',
            'url' : reverse('user:admin_dashboard'),
        }

        return render(request, 'registration/registration.html',context)


@login_required
@role_required(['superadmin','admin'])
def student(request,pk):
    """
    student sigle view
    :param request:
    """
    instance = StudentDetails.objects.get(pk=pk, is_deleted=False)
    marks = StudentMark.objects.filter(student=instance, is_deleted=False)

    context = {
        'instance': instance,
        'marks': marks,
        'page_name' : 'Student Details',
        'page_title' : 'Student Details'
    }

    return render(request, 'admin_panel/student/student.html', context)


@login_required
@role_required(['superadmin','admin'])
def students(request):
    """
    student listings
    :param request:
    :return: student list view
    """
    instances = StudentDetails.objects.filter(is_deleted=False)

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(pincode__icontains=query)
        )
        title = "StudentDetails - %s" % query
        filter_data['q'] = query

    context = {
        'instances': instances,
        'page_name' : 'Student Details',
        'page_title' : 'Student Details'
    }

    return render(request, 'admin_panel/student/student_list.html', context)


@login_required
@role_required(['superadmin','admin'])
def create_student(request):
    """
    create and update operation of student
    :param request:
    :pk for using edit each student
    :return:
    """
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
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.user = user_data
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "StudentDetails created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('user:student')
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

        form = StudentRegistrationForm()

        context = {
            'form': form,
            'page_name' : 'Create Student Details',
            'page_title' : 'Create Student Details',
            'is_need_select2' : True,
            'url' : reverse('user:create_student'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin','admin'])
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
                "redirect_url": reverse('user:students')
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
            'is_need_select2' : True,
            'url' : reverse('user:create_student'),
        }

        return render(request, 'admin_panel/create/create.html',context)



@login_required
@role_required(['superadmin','admin'])
def delete_student(request, pk):
    """
    student deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    StudentDetails.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "StudentDetails Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('user:student')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin','admin'])
def subjects(request):
    """
    subject listings
    :param request:
    :return: subject list view
    """
    instances = Subjects.objects.filter(is_deleted=False)

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query)
        )
        title = "Subjects - %s" % query
        filter_data['q'] = query

    context = {
        'instances': instances,
        'page_name' : 'Subjects',
        'page_title' : 'Subjects'
    }

    return render(request, 'admin_panel/subject/subject_list.html', context)


@login_required
@role_required(['superadmin','admin'])
def create_subject(request):
    """
    create and update operation of subject
    :param request:
    :pk for using edit each subject
    :return:
    """
    if request.method == 'POST':

        form = SubjectForm(request.POST,request.FILES)

        if form.is_valid():

            data = form.save(commit=False)
            data.auto_id = get_auto_id(Subjects)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Subjects created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('user:subject')
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

        form = SubjectForm()

        context = {
            'form': form,
            'page_name' : 'Create Subject',
            'page_title' : 'Create Subject',
            'is_need_select2' : True,
            'url' : reverse('user:create_subject'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin','admin'])
def edit_subject(request,pk):
    """
    edit operation of subject
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Subjects, pk=pk)

    message = ''
    if request.method == 'POST':
        form = SubjectForm(request.POST,instance=instance)

        if form.is_valid():

            #create subject
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Subjects created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('user:subject')
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

        form = SubjectForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Create Subjects',
            'page_title' : 'Create Subjects',
            'is_need_select2' : True,
            'url' : reverse('user:create_subject'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin','admin'])
def delete_subject(request, pk):
    """
    subject deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Subjects.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Subjects Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('user:subject')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin','admin'])
def marks(request):
    """
    mark listings
    :param request:
    :return: mark list view
    """
    instances = StudentMark.objects.filter(is_deleted=False)

    context = {
        'instances': instances,
        'page_name' : 'Student Mark',
        'page_title' : 'Student Mark'
    }

    return render(request, 'admin_panel/mark/mark_list.html', context)


@login_required
@role_required(['superadmin','admin'])
def create_mark(request, pk):
    """
    create and update operation of mark
    :param request:
    :pk for using edit each mark
    :return:
    """
    if request.method == 'POST':

        student = StudentDetails.objects.get(pk=pk, is_deleted=False)
        form = StudentMarkForm(request.POST,request.FILES)

        if form.is_valid():

            data = form.save(commit=False)
            data.auto_id = get_auto_id(StudentMark)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.student = student
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "StudentMark created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('user:student_single',kwargs={"pk":pk})
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

        form = StudentMarkForm()

        context = {
            'form': form,
            'page_name' : 'Create Subject',
            'page_title' : 'Create Subject',
            'url' : reverse('user:create_mark' , kwargs={'pk':pk}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin','admin'])
def edit_mark(request,pk,student):
    """
    edit operation of mark
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(StudentMark, pk=pk, student__pk=student)

    message = ''
    if request.method == 'POST':
        form = StudentMarkForm(request.POST,instance=instance)

        if form.is_valid():

            #create mark
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "StudentMark created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('user:student_single',kwargs={"pk":student}),
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

        form = StudentMarkForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Create Student Mark',
            'page_title' : 'Create Student Mark',
            'is_need_select2' : True,
            'url' : reverse('user:edit_mark' , kwargs={'pk':pk , "student":student}),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin','admin'])
def delete_mark(request, pk,student):
    """
    mark deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    StudentMark.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "StudentMark Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('user:student_single',kwargs={"pk":student})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')