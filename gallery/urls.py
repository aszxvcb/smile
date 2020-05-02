from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name="gallery"),
    path('newphoto/', views.photopost, name="newphoto"),
    path('newselfie/', views.selfiepost, name="newselfie"),
    path('detectphoto/', views.detectphoto, name="detectphoto"),
] 

