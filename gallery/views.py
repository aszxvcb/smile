from django.shortcuts import render
from .models import Photo

# Create your views here.
def home(request):
    return render(request, 'home2.html')

def gallery(request):
    photos = Photo.objects
    return render(request, 'gallery.html', {"photos": photos})
