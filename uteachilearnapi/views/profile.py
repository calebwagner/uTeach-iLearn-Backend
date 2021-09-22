"""View module for handling requests about park areas"""
from django.contrib.auth.models import User
from django.db import connection
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from uteachilearnapi.models import AppUser, Connection


class ProfileView(ViewSet):
    """Gamer can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and events
        """
        app_user = AppUser.objects.get(user_id=request.auth.user.id)

        app_user = AppUserSerializer(app_user, many=False, context={'request': request})

        profile = {
        'app_user': app_user.data,
        }

        return Response(profile)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post instance
        """
        try:
            app_user = AppUser.objects.get(pk=pk)
            serializer = AppUserSerializer(app_user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class AppUserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    user = UserSerializer(many=False)

    class Meta:
        model = AppUser
        fields = ['user', 'bio', 'image_url']

# class ProfileSerializer(serializers.ModelSerializer):
#     """JSON serializer for gamers"""
#     user = UserSerializer(many=False)

#     class Meta:
#         model = Connection
#         fields = ('id', 'user')



# class ConnectionSerializer(serializers.ModelSerializer):
#     """JSON serializer for gamers"""
#     user = AppUserSerializer(many=False)

#     class Meta:
#         model = Connection
#         fields = ('id', 'user', 'profile')


# class ProfileSerializer(serializers.ModelSerializer):
#     """JSON serializer for gamers"""
#     user = UserSerializer(many=False)
#     connection = ConnectionSerializer(many=False)

#     class Meta:
#         model = Connection
#         fields = ('id', 'connection', 'user')