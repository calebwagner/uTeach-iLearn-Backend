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
from rest_framework.decorators import action

class AuthorView(ViewSet):
    """Rare Authors"""

    def list(self, request):
        """Handle GET requests to authors resource
        
        Returns JSON serialized list of authors
        """
        authors = AppUser.objects.all()
        serializer = AppUserSerializer(
            authors, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single author
        Returns:
            Response -- JSON serialized author instance
        """
        try:
            author = AppUser.objects.get(pk=pk)
            serializer = AppUserSerializer(author, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(methods=['get'], detail=False)
    def getAuthor(self, request):
        user = AppUser.objects.get(user=request.auth.user)
        try:
            serializer = AppUserSerializer(user, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args[0]})

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
        fields = ['id','user', 'bio']