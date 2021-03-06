"""View module for handling requests about Messages"""
# import re
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
# from uteachilearnapi.models.post import Post
from uteachilearnapi.models.app_user import AppUser
# from uteachilearnapi.models.category import Category
from uteachilearnapi.models.message import Message


class MessageView(ViewSet):
    """uTeachiLearn Messages"""

    def list(self, request):
        """Handle GET requests to messages resource

        Returns:
            Response -- JSON serialized list of messages
        """
        messages = Message.objects.filter(recipient_id=request.auth.user.id)

        serializer = MessageSerializer(
            messages, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single message

        Returns:
            Response -- JSON serialized message instance
        """
        try:
            message = Message.objects.get(pk=pk)
            serializer = MessageSerializer(message, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations for messages

        Returns:
            Response -- JSON serialized message instance
        """
        sender = AppUser.objects.get(user=request.auth.user)
        message = Message()
        message.title = request.data["title"]
        message.description = request.data["description"]
        message.timestamp = request.data["timestamp"]
        message.read = request.data["read"]
        message.recipient = AppUser.objects.get(pk=request.data['recipient'])
        message.user = sender

        try:
            message.save()
            serializer = MessageSerializer(message, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle POST operations for messages

        Returns:
            Response -- JSON serialized message instance
        """
        sender = AppUser.objects.get(user__id=request.data["user"])
        message = Message.objects.get(pk=pk)
        message.title = request.data["title"]
        message.description = request.data["description"]
        message.timestamp = request.data["timestamp"]
        message.read = request.data["read"]
        message.user = sender
        recipient = AppUser.objects.get(pk=request.data["recipient"])
        message.recipient = recipient
        message.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        try:
            message = Message.objects.get(pk=pk)
            message.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Message.DoesNotExist as ex:
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

class RecipientSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    user = UserSerializer(many=False)

    class Meta:
        model = AppUser
        fields = ['id','user', 'image_url']

class MessageSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    user = AppUserSerializer(many=False)
    recipient = RecipientSerializer(many=False)


    class Meta:
        model = Message
        fields = ('id', 'title', 'read', 'user', 'recipient', 'timestamp', 'description')
        depth = 1
