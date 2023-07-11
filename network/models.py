from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('User', related_name='user_following', default=None)
    followers = models.ManyToManyField('User', related_name='user_followers', default=None)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    text = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes', default=None)
    edited = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user}, on {self.timestamp.strftime("%d of %b %Y, at %H:%M:%S")} wrote: "{self.text}"'
