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
    ConversationView,
    customer_task
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='homepage'),
    path('h', views.home, name='homepage'),
    path('payment/', views.add_clockin, name='add_clockin'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/', views.login_view, name='login_view'),
    path('page/', views.page, name='page'),
    path('management/', views.page, name='management'),
    path('<str:username>/createconversation/', CreateConversationView.as_view(), name='createconversation'),
    path('<str:username>/conversation/<int:pk>/', ConversationView.as_view(), name='conversation'),
    path('<str:username>/customertask/', customer_task, name='customertask'),
    path('addaccount/', views.add_AccountView),
    path('<str:MyUser_str>/', views.profile_view, name='profile'),
    # path('clock/', views.clockin_detail),
]
