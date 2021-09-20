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


class SavedPostsView(ViewSet):
    """Saved Posts View"""

    def list(self, request):
        """Handle GET requests to authors resource
        
        Returns JSON serialized list of authors
        """
        saved_posts = SavePost.objects.all()
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

class SavedPostsSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    user = AppUserSerializer(many=False)

    class Meta:
        model = SavePost
        fields = ['id','user', 'post']