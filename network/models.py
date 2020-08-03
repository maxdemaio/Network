from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    time_posted = models.DateField(auto_now_add=True)
    content = models.CharField(max_length=300)
    like_count = models.IntegerField()
