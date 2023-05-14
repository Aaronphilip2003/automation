from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('proc/', views.proc),
    path('upload/', views.upload_files, name='upload_files'),
]