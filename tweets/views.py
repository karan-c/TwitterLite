'''
 To do List:
  --> Convert functional views to class based views
'''


from http.client import responses
from django import http
from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from tweets.models import Tweet
from tweets.serializers import TweetLikeSerializer, TweetSerializer

def home_view(request, *args, **kwargs):
	return render(request=request, template_name="pages/home.html", status=200, context={})

@api_view(['GET'])
def all_tweet_api(Request, *args, **kwargs):
	tweet_list = Tweet.objects.all().order_by("-timestamp")
	serializer = TweetSerializer(tweet_list, many=True)
	return Response(serializer.data, status=200)


@api_view(['GET'])
def tweet_detail_api(Request, tweet_id, *args, **kwargs):
	try:
		tweet_obj = Tweet.objects.get(id=tweet_id)
		serializer = TweetSerializer(tweet_obj)
		return Response(serializer.data, status=200)
	except:
		return Response({ "message" : "Tweet Not Found"}, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def tweet_delete_api(Request, tweet_id, *args, **kwargs):
	tweet_obj = Tweet.objects.filter(id=tweet_id)
	if not tweet_obj.exists():
		return Response({"message": "Tweet id is invalid"}, status=400)
	tweet_obj = tweet_obj.filter(user = Request.user)
	if not tweet_obj.exists():
		return Response({"message": "User don't have permission to delete this tweet"}, status=403)
	tweet_obj = tweet_obj.first()
	tweet_obj.delete()
	return Response({"message": "Tweet deleted successfully"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_like_api(Request, *args, **kwargs):
	req_data = Request.data
	tweet_qs = Tweet.objects.filter(id=req_data.get('tweet_id'))
	if not tweet_qs.exists():
		return Response({"message": "Tweet id is invalid"}, status=400)
	tweet_obj = tweet_qs.first()
	if req_data.get('action') == 'like':
		tweet_obj.likes.add(Request.user)
	elif req_data.get('action') == 'unlike':
		tweet_obj.likes.remove(Request.user)
	return Response({"message": "Tweet liked successfully"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_api(Request, *args, **kwargs):
	serializer = TweetSerializer(data=Request.data)
	print(Request)
	if serializer.is_valid(raise_exception=True):
		serializer.save(user=Request.user)
		return Response(serializer.data, status=200)
	return Response({"message": "Bad Request"}, status=400)