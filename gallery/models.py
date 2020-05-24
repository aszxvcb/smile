from django.db import models
from django.utils import timezone
from django.conf import settings
import os

# Create your models here.
def unique_file_name(instance, filename):
    current_time = instance.created_date
    time_info  = current_time.strftime('%y%m%d%H%M%S')
    root_ext = os.path.splitext(filename)   #filename "file.jpg"에서 "." 기준으로 잘라서 "file" ".jpg"과 같이 나누어 root_ext에 저장

    instance_type = type(instance)
    if instance_type is Photo:
        return 'unknown/{0}_{1}{2}'.format(root_ext[0], time_info, root_ext[1])
    elif instance_type is Selfie:
        user_name = instance.owner.username
        return 'known/{0}/{1}_{2}{3}'.format(user_name, root_ext[0], time_info, root_ext[1])




class Photo(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=unique_file_name)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.owner.username + "_" + str(self.created_date)


class Selfie(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=unique_file_name)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        current_time = self.created_date
        time_info  = current_time.strftime('%y%m%d%H%M%S')
        return "selfie_" + self.owner.username + "_" + time_info

