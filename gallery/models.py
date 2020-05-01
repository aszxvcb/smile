from django.db import models
from django.utils import timezone
from django.conf import settings
import os
# from django.contrib import auth


# Create your models here.

def unique_file_name(instance, filename):
    current_time = instance.created_date.today()
    time_info  = current_time.strftime('%y%m%d%H%M%S')
    root_ext = os.path.splitext(filename)   #filename "file.jpg"에서 "." 기준으로 잘라서 "file" ".jpg"과 같이 나누어 root_ext에 저장
    return 'images/{0}_{1}{2}'.format(root_ext[0], time_info, root_ext[1])

class Photo(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='images/')
    image = models.ImageField(upload_to= unique_file_name)

    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.username + "_" + str(self.created_date)
    #     # return self.image.name + "_" + str(self.created_date)


class Selfie(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=unique_file_name)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        current_time = self.created_date.today()
        time_info  = current_time.strftime('%y%m%d%H%M%S')
        return "Selfie_" + self.owner.usernmae + "_" + time_info