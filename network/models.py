from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follows')
    followed_at = models.TimeField(auto_now=True)

# class Follower(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_followed')
#     follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows_user')
#     followed_at = models.TimeField(auto_now=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="liked_by")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='likes', blank=True, null=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post', null=True)
    content = models.CharField(max_length=64)
    timestamp = models.TimeField(auto_now=True)
    like = models.IntegerField(default=0)

    def serialize(self):
        return {
            'user': self.user.username,
            "content": self.content,
            "timestamp": self.timestamp,
            "likes": self.like,
        }







