from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from .models import User
from .serializers import UserCreateSerializer

@api_view(['POST'])
def register_user(Request, *args, **kwargs):
    user_serializer = UserCreateSerializer(data=Request.data)
    if user_serializer.is_valid():
        user_instance = user_serializer.save()
        if user_instance:
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
