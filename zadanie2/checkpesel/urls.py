from django.urls import path, include
from . import views


app_name = 'checkpesel'

urlpatterns = [
    path('', views.upload_pesel, name='upload_pesel'),
    path('result/', views.result, name='result'),
]
