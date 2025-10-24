from django.urls import path
from . import views

app_name = 'textshuffle'

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('result/', views.result, name='result'),
]