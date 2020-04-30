from django.db import models
from django.utils import timezone
from django.conf import settings
# from django.contrib import auth


# Create your models here.

def unique_file_name(instance, filename):
    return 'images/{0}_{1}'.format(filename, str(instance.created_date))

class Photo(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='images/')
    image = models.ImageField(upload_to= unique_file_name)

    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.username + "_" + str(self.created_date)
    #     # return self.image.name + "_" + str(self.created_date)