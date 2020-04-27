from django.shortcuts import render, redirect
from .models import Photo
from .forms import PhotoPost
from django.utils import timezone

# Create your views here.
def home(request):
    return render(request, 'home2.html')

def gallery(request):
    photos = Photo.objects
    return render(request, 'gallery.html', {"photos": photos})

def photopost(request):
    if request.method == 'POST':
        form = PhotoPost(request.POST, request.FILES)
        # print(form.is_valid())
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = timezone.now()
            # post.user = request.user
            post.save()
            return redirect('gallery')
    else :
        form = PhotoPost()
        return render(request, 'new.html', {"form": form})