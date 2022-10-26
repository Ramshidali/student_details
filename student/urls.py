from . import views
from django.urls import path, re_path

# Create your tests here.

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.index, name="student_dashboard"),
    path('registration/', views.student_registration, name="student_registration"),

    re_path(r'^edit-student/(?P<pk>.*)/$', views.edit_student, name='edit_student'),

]