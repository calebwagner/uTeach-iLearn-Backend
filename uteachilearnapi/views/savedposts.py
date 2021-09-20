"""View module for handling requests about authors"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from uteachilearnapi.models.app_user import AppUser
from django.contrib.auth.models import User
from uteachilearnapi.models.savepost import SavePost
from uteachilearnapi.models.post import Post


class SavedPostsView(ViewSet):
    """Saved Posts View"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized connections instance
        """
        user = AppUser.objects.get(user=request.auth.user)
        # profile = AppUser.objects.get(pk=request.data['profile'])


        save_post = SavePost()
        save_post.user = user
        save_post.post = Post.objects.get(pk=request.data['post'])
        # connection.profile = AppUser.objects.filter(profile=request.auth.user.id)

        try:
            save_post.save()
            serializer = SavedPostsSerializer(save_post, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single connection
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            saved_post = SavePost.objects.get(pk=pk)
            saved_post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except SavePost.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post instance
        """
        try:
            saved_post = SavePost.objects.get(pk=pk)
            serializer = SavedPostsSerializer(saved_post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to authors resource
        
        Returns JSON serialized list of authors
        """
        saved_posts = SavePost.objects.filter(user_id=request.auth.user.id)
        serializer = SavedPostsSerializer(
            saved_posts, many=True, context={'request': request})
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'username')

class AppUserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    user = UserSerializer(many=False)

    class Meta:
        model = AppUser
        fields = ['id','user']

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    user = AppUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'user',
                  'created_on', 'image', 'description')
        depth = 1

class SavedPostsSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    user = AppUserSerializer(many=False)
    post = PostSerializer(many=False)

    class Meta:
        model = SavePost
        fields = ['id','user', 'post']