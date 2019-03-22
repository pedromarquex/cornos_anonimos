from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Cuck(models.Model):
    # user must be lowercase
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # nick must be lowercase
    nick = models.CharField(max_length=20)

    def __str__(self):
        return self.nick
