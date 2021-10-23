from http.client import responses
from django import http
from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request
from tweets.models import Tweet
from tweets.serializers import TweetSerializer

# Create your views here.
def home_view(request, *args, **kwargs):
	return render(request=request, template_name="pages/home.html", status=200, context={})

def all_tweet_api(request, *args, **kwargs):
	tweet_list = Tweet.objects.all()
	data = [{"id": x.id, "content": x.content} for x in tweet_list]
	res = {
		"response": data
	}
	return JsonResponse(res)

@api_view(['GET'])
def tweet_detail_api(Request, tweet_id, *args, **kwargs):
	try:
		tweet_obj = Tweet.objects.get(id=tweet_id)
		serializer = TweetSerializer(tweet_obj)
		return Response(serializer.data, status=200)
	except:
		return Response({ "message" : "Tweet Not Found"}, status=400)

@api_view(['GET'])
def tweet_delete_api(Request, tweet_id, *args, **kwargs):
	try:
		tweet_obj = Tweet.objects.get(id=tweet_id)
		tweet_obj.delete()
		return Response({"message": "Tweet deleted successfully"}, status=200)
	except:
		return Response({"message": "Tweet id is invalid"}, status=400)

@api_view(['POST'])
def tweet_create_api(Request, *args, **kwargs):
	serializer = TweetSerializer(data=Request.data)
	print(Request)
	if serializer.is_valid(raise_exception=True):
		serializer.save()
		return Response(serializer.data, status=200)
	return Response({"message": "Bad Request"}, status=400)