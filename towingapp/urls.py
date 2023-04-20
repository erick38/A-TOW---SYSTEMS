from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='indexone'),
    # path('form/', views.add_message),
    path('login/', views.login_view, name='login_view'),
    
]