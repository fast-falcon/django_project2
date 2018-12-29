"""Webeloperss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Webeloperss import settings
from webapp import views

urlpatterns = [
    path('reset/', views.reset),
    path('forgot/', views.forgot),
    path('search_teachers_api/', views.search_teachers),
    path('editprofile/', views.editprofile),
    path('createmeeting/', views.createmeeting),
    path('removeuser/', views.removeuser),
    path('search/', views.search),
    path('profile/', views.profile),
    path('contactus/', views.contactus),
    path('logout/', views.logout_),
    path('login/', views.login_),
    path('signup/', views.signup),
    path('', views.main),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)