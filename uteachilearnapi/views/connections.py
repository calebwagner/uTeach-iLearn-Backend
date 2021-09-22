"""View module for handling requests about categories"""
from django.db import connection
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.db.models import fields
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from uteachilearnapi.models.post import Post
from uteachilearnapi.models.app_user import AppUser
from uteachilearnapi.models import Connection
from django.contrib.auth.models import User


class ConnectionView(ViewSet):
    """[summary]

    Args:
        ViewSet ([type]): [description]
    """
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized connections instance
        """
        user = AppUser.objects.get(user=request.auth.user)
        # profile = AppUser.objects.get(pk=request.data['profile'])


        connection = Connection()
        connection.user = user
        connection.profile = AppUser.objects.get(pk=request.data['profile'])
        # connection.profile = AppUser.objects.filter(profile=request.auth.user.id)

        try:
            connection.save()
            serializer = ConnectionSerializer(connection, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET requests to connection resource
        Returns:
            Response -- JSON serialized list of connection
        """
        connection = Connection.objects.filter(user_id=request.auth.user.id)

        serializer = ConnectionSerializer(connection, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            connection = Connection.objects.get(pk=pk)
            serializer = ConnectionSerializer(connection, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single connection
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            connection = Connection.objects.get(pk=pk)
            connection.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Connection.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users name"""
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email']


class AppUserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    user = UserSerializer(many=False)

    class Meta:
        model = AppUser
        fields = ['id','user', 'image_url']

class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    user = UserSerializer(many=False)

    class Meta:
        model = AppUser
        fields = ['id','user', 'image_url']

class ConnectionSerializer(serializers.ModelSerializer):
    """JSON serializer for connection
    Arguments:
        serializer type
    """
    user = AppUserSerializer(many=False)
    profile = ProfileSerializer(many=False)


    class Meta:
        model = Connection
        fields = ('id', 'user', 'profile')
        depth: 1