from django.shortcuts import render, redirect
from .models import Photo
from .forms import PhotoPost, SelfiePost
from django.utils import timezone
from django.contrib import messages

# Create your views here.
def home(request):
    messages.info(request, "home 화면입니다")
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
            post.owner = request.user
            post.save()
            messages.info(request, "저장 성공!")
            return redirect('gallery')
    else :
        form = PhotoPost()
        return render(request, 'new.html', {"form": form})

def selfiepost(request):
    if request.method == "POST":
        form = SelfiePost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('gallery')
    else :
        form = SelfiePost()
        return render(request, 'new.html', {"form": form })