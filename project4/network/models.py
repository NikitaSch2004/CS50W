from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Postare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True,default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

    def total_likes(self):
        return self.likes.count()
        
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')  # Ensure unique pairs (follower, followed)

    def __str__(self):
        return f'{self.follower.username} follows {self.followed.username}'
    
    def serialize(self):
        return {
            "follower": self.follower,
            "followed": self.followed,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }