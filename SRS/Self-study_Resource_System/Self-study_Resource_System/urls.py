"""
URL configuration for Self-study_Resource_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from dashboard import views as dash_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views

from django.http import HttpResponseForbidden

# def restrict_admin_ips(get_response):
#     def middleware(request):
#         allowed_ips = ['152.58.16.40', '::1']  # Add your trusted IPs here
#         if request.path.startswith('/admin') and request.META['REMOTE_ADDR'] not in allowed_ips:
#             return HttpResponseForbidden("Access Denied")
#         return get_response(request)
#     return middleware

# MIDDLEWARE = ['Self-study_Resource_System.middleware.restrict_admin_ips'] + MIDDLEWARE




urlpatterns = [
    # path('secure-admin-1234/', admin.site.urls),   # for ngrok server
    path('admin/', admin.site.urls),   # for local server
    path('',include('dashboard.urls')),
    # path('register/',dash_views.register,name='register'),
    path('register/',dash_views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name="dashboard/login.html"),name='login'),
    path('', views.register, name='home'),
    path('logout/',auth_views.LogoutView.as_view(template_name="dashboard/logout.html"),name='logout'),
    path('profile/',dash_views.profile,name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
