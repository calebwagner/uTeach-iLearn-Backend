"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import connection
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action
from uteachilearnapi.models.app_user import AppUser
from uteachilearnapi.models.meeting import Meeting
from uteachilearnapi.models.connection import Connection


class MeetingView(ViewSet):

    def create(self, request):
        """Handle POST operations for events
        Returns:
            Response -- JSON serialized event instance
        """
        scheduler = AppUser.objects.get(user=request.auth.user)

        meeting = Meeting()
        meeting.connection = Connection.objects.get(pk=request.data['connection'])
        # meeting.connection = AppUser.objects.get(pk=request.data['connection'])
        meeting.description = request.data["description"]
        meeting.created_on = request.data["created_on"]
        meeting.scheduled_date = request.data["scheduled_date"]
        meeting.scheduler = scheduler

        try:
            meeting.save()
            serializer = MeetingSerializer(meeting, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            meeting = Meeting.objects.get(pk=pk)
            serializer = MeetingSerializer(meeting, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            meeting = Meeting.objects.get(pk=pk)
            meeting.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Meeting.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to posts resource

        Returns:
            Response -- JSON serialized list of posts
        """
        # Get all game records from the database
        meetings = Meeting.objects.filter(scheduler_id=request.auth.user.id)

        serializer = MeetingSerializer(
            meetings, many=True, context={'request': request})
        return Response(serializer.data)


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

class ConnectionSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    profile = AppUserSerializer(many=False)

    class Meta:
        model = Connection
        fields = ['id', 'profile']

class MeetingSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    scheduler = AppUserSerializer(many=False)
    connection = ConnectionSerializer(many=False)

    class Meta:
        model = Meeting
        fields = ('id', 'scheduler', 'connection', 'description', 'created_on','scheduled_date')
        depth = 1