from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


# New Post
class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post")
    body = models.TextField(blank=True)
    like_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.user.id,
            "body": self.body,
            "like_count": self.like_count,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profile")
    user_bio = models.TextField(blank=True)
    following = models.ManyToManyField("User", related_name="following_users")
    followers = models.ManyToManyField("User", related_name="followers_users")

    def serialize(self, user):
        return {
            "id": self.id,
            "username": self.user.username,
            "following": self.followers.count(),
            "followers": self.followers.count(),
        }

