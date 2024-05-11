from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Picture, Like, Follow
from .serializers import UserSerializer, PictureSerializer, LikeSerializer, FollowSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PictureListView(APIView):
    def get(self, request):
        pictures = Picture.objects.all().order_by('-created_at')  # Sort by latest first
        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data)

class PictureDetailView(APIView):
    def get(self, request, pk):
        try:
            picture = Picture.objects.get(pk=pk)
        except Picture.DoesNotExist:
            return Response({'error': 'Picture not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)

class PictureCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PictureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Associate picture with authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            picture = Picture.objects.get(pk=pk)
        except Picture.DoesNotExist:
            return Response({'error': 'Picture not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        like, created = Like.objects.get_or_create(user=user, picture=picture)

        if not created:  # User already liked the picture, so unlike
            like.delete()
            return Response({'message': 'Unliked'}, status=status.HTTP_200_OK)

        return Response({'message': 'Liked'}, status=status.HTTP_201_CREATED)

class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user_to_follow = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        follower = request.user

        if follower == user_to_follow:  # User cannot follow themself
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=follower, following=user_to_follow)

        if not created:  # User already follows, so unfollow
            follow.delete()
            return Response({'message': 'Unfollowed'}, status=status.HTTP_200_OK)

        return Response({'message': 'Followed'}, status=status.HTTP_201_CREATED)

class FollowingFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        following_list = user.following.all()
        pictures = Picture.objects.filter(user__in=following_list).order_by('-created_at')
        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data)
