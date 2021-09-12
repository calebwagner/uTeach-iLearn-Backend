"""View module for handling requests about posts"""
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from uteachilearnapi.models.post import Post
from uteachilearnapi.models.app_user import AppUser
from uteachilearnapi.models.category import Category


class PostView(ViewSet):
    """uTeachiLearn Posts"""

    def list(self, request):
        """Handle GET requests to posts resource

        Returns:
            Response -- JSON serialized list of posts
        """
        # Get all game records from the database
        posts = Post.objects.all()

        # FOREIGN KEYS
        category = self.request.query_params.get('category', None)
        if category is not None:
            posts = posts.filter(category__id=category)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post instance
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations for posts

        Returns:
            Response -- JSON serialized post instance
        """
        app_user = AppUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])

        post = Post()
        post.title = request.data["title"]
        post.description = request.data["description"]
        post.created_on = request.data["created_on"]
        post.image = request.data["image"]
        post.user = app_user
        post.category = category

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle POST operations for posts

        Returns:
            Response -- JSON serialized post instance
        """
        app_user = AppUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])

        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.description = request.data["description"]
        post.created_on = request.data["created_on"]
        post.image = request.data["image"]
        post.user = app_user
        category = Category.objects.get(pk=request.data["category"])
        post.category = category
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users name"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AppUserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    user = UserSerializer(many=False)

    class Meta:
        model = AppUser
        fields = ['user']


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    user = AppUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'user',
                  'created_on', 'image', 'description')
        depth = 1
