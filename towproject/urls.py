"""towproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from towingapp import views
from towingapp.views import (
    CreateConversationView,
    customer_task,
    combined_form,
    save_location,
    success,
    gps,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('h', views.home, name='homepage'),
    path('payment/', views.add_clockin, name='add_clockin'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/', views.login_view, name='login_view'),
    path('management/', views.submit, name='management'),
    path('createconversation/', CreateConversationView, name='createconversation'),
    path('<str:username>/customertask/', customer_task, name='customertask'),
    path('addaccount/', views.add_AccountView),
    path('combined/form/submit/', views.submit, name='submit'),
    path('save_location/', save_location, name='save_location'),
    path('success/<str:identifier>/', success, name='success'),
    path('gps/', gps, name='gps'),
    path('<str:MyUser_str>/', views.profile_view, name='profile'),
    path('combined/form/', combined_form, name='combined_form'),
    # path('clock/', views.clockin_detail),
]
