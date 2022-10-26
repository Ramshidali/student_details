from django.contrib import admin
from django.views.static import serve
from django.urls import include, path, re_path
from main import views as general_views

from student_details import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/accounts/', include('registration.backends.default.urls')),
    path('app/',general_views.app,name='app'),
    path('super-admin/',include(('main.urls'),namespace='main')),

    path('student/',include(('student.urls'),namespace='student')),
    path('user/',include(('user.urls'),namespace='user')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
