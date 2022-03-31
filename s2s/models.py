import random
from django.conf import settings
from django.db import models
from django.db.models import Q

User = settings.AUTH_USER_MODEL # auth.User

Product_Items = ['Tesla', 'Iphone', 'private jet', 'Macbook']

class s2sModel(models.Model):

    title = models.CharField(max_length=120)
    def get_title(self):
        return "title"
