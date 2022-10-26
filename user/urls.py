from . import views
from django.urls import path, re_path

# Create your tests here.

app_name = 'user'

urlpatterns = [
    path('dashboard/', views.index, name="admin_dashboard"),

    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('registration/', views.admin_registration, name="admin_registration"),

    path('student/', views.students, name='student'),
    re_path(r'^student/(?P<pk>.*)/$', views.student, name='student_single'),
    re_path(r'^create-student/$', views.create_student, name='create_student'),
    re_path(r'^edit-student/(?P<pk>.*)/$', views.edit_student, name='edit_student'),
    re_path(r'^delete-student/(?P<pk>.*)/$', views.delete_student, name='delete_student'),

    path('subject/', views.subjects, name='subject'),
    re_path(r'^create-subject/$', views.create_subject, name='create_subject'),
    re_path(r'^edit-subject/(?P<pk>.*)/$', views.edit_subject, name='edit_subject'),
    re_path(r'^delete-subject/(?P<pk>.*)/$', views.delete_subject, name='delete_subject'),

    path('marks/', views.marks, name='marks'),
    re_path(r'^create-mark/(?P<pk>.*)/$', views.create_mark, name='create_mark'),
    re_path(r'^edit-mark/(?P<pk>.*)/(?P<student>.*)/$', views.edit_mark, name='edit_mark'),
    re_path(r'^delete-mark/(?P<pk>.*)/(?P<student>.*)/$', views.delete_mark, name='delete_mark'),

]