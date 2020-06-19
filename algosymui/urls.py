"""algosymui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib import admin

from authuser.views import RegisterView
from ui.views import main, create, remove, save, change_name, run


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="auth/login.html"),
         name='login'),
    path('register/', RegisterView.as_view(),
         name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page="/"), name="logout"),

    path('', main, name='index'),
    path('create/', create, name="algo-create"),
    path('delete/', remove, name="algo-remove"),
    path('save/', save, name="algo-save"),
    path('run/', run, name="algo-run"),
    path('change/name/', change_name, name="algo-change-name"),

    path('admin/', admin.site.urls),
]

