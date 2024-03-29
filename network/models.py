from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass



# New Post
class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post")
    username = models.TextField(blank=True)
    body = models.TextField(blank=True)
    like_count = models.IntegerField(default=0)
    liked_by = models.ManyToManyField("User", related_name="post_liked_by")
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.user.id,
            "username": self.username,
            "body": self.body,
            "like_count": self.like_count,
            "liked_by": self.liked_by,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

class Profile(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_profile")
    username= models.TextField(blank=True)
    user_bio = models.TextField(blank=True)
    following = models.ManyToManyField("User", related_name="following_users")
    followers = models.ManyToManyField("User", related_name="followers_users")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "following": self.followers.count(),
            "followers": self.followers.count(),
        }

