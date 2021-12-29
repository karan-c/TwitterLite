from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from .models import User
from .serializers import UserCreateSerializer, UserDetailsSerializer

@api_view(['POST'])
def register_user(Request, *args, **kwargs):
    user_serializer = UserCreateSerializer(data=Request.data)
    if user_serializer.is_valid():
        user_instance = user_serializer.save()
        if user_instance:
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_details(Request, user_id, *args, **kwargs):
    user_obj = User.objects.filter(id = user_id)
    if not user_obj.exists():
        return Response({"message": "Invalid user id"}, status=status.HTTP_404_NOT_FOUND)
    user_serializer = UserDetailsSerializer(user_obj.first())
    return Response(user_serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user(Request, *args, **kwargs):
    req_data = Request.data
    user_obj = User.objects.filter(id = req_data.get('id'))
    if not user_obj.exists():
        return Response({"message": "Invalid User id"}, status=status.HTTP_404_NOT_FOUND)
    user_obj = user_obj.first()
    if 'first_name' in req_data:
        user_obj.first_name = req_data.get('first_name')
    if 'last_name' in req_data:
        user_obj.last_name = req_data.get('last_name')
    if 'bio' in req_data:
        user_obj.bio = req_data.get('bio')
    user_obj.save()
    user_serializer = UserDetailsSerializer(user_obj)
    return Response(user_serializer.data, status=status.HTTP_200_OK)
