from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Provide unique related_name attributes for groups and user_permissions
    # to avoid clashes with the default User model.
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user',
    )

class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pictures')
    image_url = models.URLField()  # Store image URL instead of base64 string for flexibility
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically record creation time

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='likes')

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'following')  # Enforce unique follower-following pairs
