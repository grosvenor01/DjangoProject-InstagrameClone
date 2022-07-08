import uuid
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
User=get_user_model()
class profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user =models.IntegerField()
    profile_pic=models.ImageField(upload_to='profile_pics' , default='blank.jpg')
    location=models.CharField(max_length=200,default='none')
    bio=models.TextField()
    def __str__(self):
        return self.user.username
class post(models.Model):
    id=models.UUIDField(primary_key=True,default= uuid.uuid4)
    nbr_like=models.IntegerField(default=0)
    user=models.CharField(max_length=150)
    caption=models.TextField()
    date=models.DateTimeField(default=datetime.now)
    image=models.ImageField(upload_to='posts')
    def __str__(self):
        return self.user
class like(models.Model):
    id_post=models.CharField(max_length=500)
    usernam=models.CharField(max_length=200)
    def __str__(self):
        return self.usernam
class followers(models.Model):
    user=models.CharField(max_length=200)
    followers=models.CharField(max_length=200)
    def __str__(self):
        return self.user