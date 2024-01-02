from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .serializers import UserRegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        user_serializer = UserRegisterSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data="User Registered Successfully", status=status.HTTP_201_CREATED)
        else:
            return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView, PageNumberPagination):
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        if user:
            user_serializer = UserSerializer(instance=user)
            user_data = user_serializer.data
            return Response(data=user_data, status=status.HTTP_200_OK)
        else:
            data = {"error": "user not found"}
            return Response(data=data, status=status.HTTP_400_BAD)

    def list(self, request):
        users = User.objects.all()
        user_of_this_page = self.paginate_queryset(users, request)
        user_serializer = self.serializer(instance=user_of_this_page, many=True)
        user_data = user_serializer.data
        user_paginated_data = self.get_paginated_response(user_data)
        return Response(data=user_paginated_data, status=status.HTTP_200_OK)




