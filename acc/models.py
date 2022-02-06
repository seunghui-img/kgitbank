from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    comment = models.TextField()
    age = models.IntegerField(default=0)

    # upload_to : 업로드될 폴더명으로 media/user/2022에 쌓이게 된다
    pic = models.ImageField(upload_to="user/%y")

    def getpic(self):
        if self.pic:
            return self.pic.url
        return "/media/noimage.png"
