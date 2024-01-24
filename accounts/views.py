from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.views import Response, APIView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes
from .serializers import UserRegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        user_serializer = UserRegisterSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                data="User Registered Successfully", status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema_view(
    get=extend_schema(
        summary="Get the current user",
        responses={200: UserSerializer},
        tags=["User"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a user by ID",
        responses={
            200: UserSerializer,
            404: OpenApiResponse(
                OpenApiTypes.OBJECT,
                "bad request",
                [
                    OpenApiExample(
                        name="User not found",
                        value={"error": "user not found"},
                    )
                ],
            ),
        },
        tags=["User"],
    ),
    list=extend_schema(
        summary="List all users",
        parameters=[
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page number for pagination",
            ),
        ],
        responses={200: [UserSerializer]},
        tags=["User"],
    ),
)
class UserViewSet(viewsets.ViewSet, PageNumberPagination):
    def get_permissions(self):
        if self.action == "get":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    serializer_class = UserSerializer

    @action(detail=False, url_path="current")
    def get(self, request):
        user = request.user
        if user:
            user_serializer = self.serializer_class(instance=user)
            user_data = user_serializer.data
            return Response(data=user_data, status=status.HTTP_200_OK)
        else:
            data = {"error": "user not found"}
            return Response(data=data, status=status.HTTP_400_BAD)

    def retrieve(self, request, pk):
        user = User.objects.get(pk=pk)
        if user is None:
            return Response(
                data={"error": "user not found"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            user_serializer = self.serializer_class(instance=user)
            user_data = user_serializer.data
            return Response(data=user_data, status=status.HTTP_200_OK)

    def list(self, request):
        users = User.objects.all()
        user_of_this_page = self.paginate_queryset(users, request)
        user_serializer = self.serializer_class(instance=user_of_this_page, many=True)
        user_data = user_serializer.data
        return self.get_paginated_response(user_data)
