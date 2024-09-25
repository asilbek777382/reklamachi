from django.db import models

# Create your models here.

from django.utils import timezone

default_value = timezone.now()


from django.db import models
from django.utils import timezone

class MyModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)



class kirish(models.Model):
    login=models.CharField(max_length=30)
    parol = models.CharField(max_length=30)
    user_id = models.IntegerField(default=0)


class set_message(models.Model):
    gurux_id= models.CharField(max_length=30,default=0)
    users_id= models.CharField(max_length=30,default=0)
    xolati=models.CharField(max_length=30)
    matn=models.CharField(max_length=200)
    rasm = models.ImageField(uploadd_to='images/')
    video = models.FileField(upload_to='videos/')
    url_tugmachalar=models.CharField(max_length=200)
    vaqt= models.CharField(max_length=30)
    tugash_sanasi=models.CharField(max_length=30)
    xabarni_qadash=models.CharField(max_length=30)
    songgi_xabarni_ochirish=models.CharField(max_length=30)
