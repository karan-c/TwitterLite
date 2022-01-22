from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from .models import User
from .serializers import UserCreateSerializer, UserDetailsSerializer
from requests import request
from django.conf import settings

def image_upload(base64):
	imgur_api = 'https://api.imgur.com/3/image'
	body = {
		'image': base64
	}
	headers = {
		'Authorization': 'Client-ID ' + settings.IMGUR_CLIENT_ID
	}
	files = []
	response = request("POST", imgur_api, headers=headers, data=body, files=files)
	return response.json()

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

@api_view(['GET'])
def user_details_by_user_name(Request, user_name, *args, **kwargs):
    user_obj = User.objects.filter(user_name=user_name)
    if not user_obj.exists():
        return Response({"message": "Invalid user id"}, status=status.HTTP_404_NOT_FOUND)
    user_obj = user_obj.first()
    user_serializer = UserDetailsSerializer(user_obj)
    response_data = user_serializer.data
    if Request.user and Request.user != user_obj:
        follower = user_obj.followers.filter(user_name = Request.user)
        response_data['already_following'] = True if follower.exists() else False
    else:
        response_data['already_following'] = False
    return Response(response_data, status=status.HTTP_200_OK)

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
    if 'user_name' in req_data and req_data.get('user_name') != user_obj.user_name:
        user_exists = User.objects.filter(user_name = req_data.get('user_name'))
        if user_exists.exists():
            return Response({"message": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user_obj.user_name = req_data.get('user_name')
    if 'profile_pic' in req_data:
        response = image_upload(req_data.get('profile_pic'))
        if response.get('status') == 200:
            user_obj.profile_pic = response.get('data').get('link')
            user_obj.profile_pic_hash = response.get('data').get('deletehash')
        else:
            return Response({"message": "Something went wrong while uploading image. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    user_obj.save()
    user_serializer = UserDetailsSerializer(user_obj)
    return Response(user_serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(Request, *args, **kwargs):
    req_data = Request.data
    following_user = User.objects.filter(id = req_data.get("id"))
    follower_user = User.objects.filter(user_name = Request.user)
    if not follower_user.exists() or not following_user.exists():
        return Response({"message": "Invalid users details"}, status=status.HTTP_404_NOT_FOUND)
    follower_user = follower_user.first()
    following_user = following_user.first()
    follower_exists = follower_user.followings.filter(id = following_user.id)
    if follower_exists.exists():
        follower_user.followings.remove(following_user)
    else:
        follower_user.followings.add(following_user)
    follower_user.save()
    return Response({"message": "Followers updated successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_followers_list(Request, user_id, *args, **kwargs):
    user_obj = User.objects.filter(id = user_id)
    if not user_obj.exists():
        return Response({"message": "Invalid User id"}, status=status.HTTP_404_NOT_FOUND)
    user_obj = user_obj.first()
    followers_list = user_obj.followers.all()
    user_serializer = UserDetailsSerializer(followers_list, many=True)
    return Response(user_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_followings_list(Request, user_id, *args, **kwargs):
    user_obj = User.objects.filter(id = user_id)
    if not user_obj.exists():
        return Response({"message": "Invalid User id"}, status=status.HTTP_404_NOT_FOUND)
    user_obj = user_obj.first()
    followings_list = user_obj.followings.all()
    user_serializer = UserDetailsSerializer(followings_list, many=True)
    return Response(user_serializer.data, status=status.HTTP_200_OK)
