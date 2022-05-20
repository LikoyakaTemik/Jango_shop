from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class Product(models.Model):
    label = models.CharField(max_length=20)
    price = models.IntegerField()
    url_img = models.URLField()
    id_user = models.IntegerField()

class Message(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField(max_length=255)