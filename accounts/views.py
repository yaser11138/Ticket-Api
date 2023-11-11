from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from .serializers import UserRegisterSerializer


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





