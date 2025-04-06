from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Todo
from .serializers import TodoSerializer

class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Swagger decorator for GET and POST operations
    @swagger_auto_schema(
        operation_description="Get the list of todos for the authenticated user",
        responses={200: TodoSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new todo item",
        request_body=TodoSerializer,
        responses={201: TodoSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        # Only return todos for the authenticated user
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save the todo item with the authenticated user
        serializer.save(user=self.request.user)


class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a specific todo item",
        responses={200: TodoSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific todo item",
        request_body=TodoSerializer,
        responses={200: TodoSerializer},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific todo item",
        responses={204: 'No Content'},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionDenied("Forbidden")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Forbidden")
        instance.delete()
