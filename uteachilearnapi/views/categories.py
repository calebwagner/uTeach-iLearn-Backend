"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.db.models import fields
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from uteachilearnapi.models import Category

class CategoryView(ViewSet):
    """[summary]

    Args:
        ViewSet ([type]): [description]
    """
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized game instance
        """
        category = Category()
        category.title = request.data["title"]
        category.description = request.data["description"]

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET requests to category resource
        Returns:
            Response -- JSON serialized list of category
        """
        category = Category.objects.all()

        serializer = CategorySerializer(category, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single category
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a category
        Returns:
            Response -- Empty body with 204 status code
        """
        category = Category.objects.get(pk=pk)

        category.title = request.data["title"]
        category.description = request.data["description"]

        category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    Arguments:
        serializer type
    """
    class Meta:
        model = Category
        fields = ('id', 'title', 'description')