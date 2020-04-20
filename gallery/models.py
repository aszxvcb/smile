from django.db import models
from django.utils import timezone

# Create your models here.
class Photo(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.owner.username + "_" + str(self.created_date)
