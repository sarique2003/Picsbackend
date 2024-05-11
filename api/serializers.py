from rest_framework import serializers
from .models import User, Picture, Like, Follow

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class PictureSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)  # Include user details

    class Meta:
        model = Picture
        fields = ('id', 'image_url', 'created_at', 'user', 'likes_count')

    def get_likes_count(self, obj):
        return obj.likes.count()

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'picture')  # Might not be needed for all API endpoints

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following')
