#standerd
import datetime
#django
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from main.decorators import role_required
#local


# @check_mode

@login_required
def app(request):

    return HttpResponseRedirect(reverse('main:index'))

# Create your views here.

@login_required
@role_required(['superadmin','admin'])
def index(request):
    today = datetime.date.today()

    context = {
        'page_name' : 'Dashboard',
    }

    return render(request,'admin_panel/index.html', context)