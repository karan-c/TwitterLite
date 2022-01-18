'''
 To do List:
  --> Convert functional views to class based views
'''


from email import header
from os import stat
from django.shortcuts import render
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination 
from tweets.models import Tweet
from tweets.serializers import TweetDetailSerializer, TweetLikeSerializer, TweetCreateSerializer
from users.models import User
from requests import request

def home_view(request, *args, **kwargs):
	return render(request=request, template_name="pages/home.html", status=status.HTTP_200_OK, context={})

def image_upload(base64):
	imgur_api = 'https://api.imgur.com/3/image'
	body = {
		'image': base64
	}
	headers = {
		'Authorization': 'Client-ID 6098f21a05cc688'
	}
	files = []
	response = request("POST", imgur_api, headers=headers, data=body, files=files)
	return response.json()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10
class TweetLists(generics.ListAPIView):
	queryset = Tweet.objects.all().order_by("-timestamp")
	serializer_class = TweetDetailSerializer
	pagination_class = StandardResultsSetPagination

	# def get_serializer_context(self):
	# 	print(Request.user)
	# 	return {
	# 		"user_name": Request.user
	# 	}

@api_view(['GET'])
def tweet_detail_api(Request, tweet_id, *args, **kwargs):
	try:
		tweet_obj = Tweet.objects.get(id=tweet_id)
		serializer = TweetDetailSerializer(tweet_obj, context={"user_name": Request.user})
		return Response(serializer.data, status=status.HTTP_200_OK)
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
	return Response({"message": "Tweet deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_like_api(Request, *args, **kwargs):
	req_data = Request.data
	tweet_qs = Tweet.objects.filter(id=req_data.get('tweet_id'))
	if not tweet_qs.exists():
		return Response({"message": "Tweet id is invalid"}, status=status.HTTP_404_NOT_FOUND)
	tweet_obj = tweet_qs.first()
	if req_data.get('action') == 'like':
		tweet_obj.likes.add(Request.user)
	elif req_data.get('action') == 'unlike':
		tweet_obj.likes.remove(Request.user)
	return Response({"message": "Tweet liked successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def retweet_api(Request, *args, **kwargs):
	req_data = Request.data
	tweet_qs = Tweet.objects.filter(id=req_data.get('tweet_id'))
	if not tweet_qs.exists():
		return Response({"message": "Tweet id is invalid"}, status=status.HTTP_404_NOT_FOUND)
	tweet_obj = tweet_qs.first()
	tweet_obj.retweet_count += 1
	tweet_obj.save()
	new_tweet = None
	if 'image' in req_data:
		response = image_upload(req_data.get('image'))
		if response.get('status') == 200:
			new_tweet = Tweet.objects.create (
				user=Request.user,
				retweet_obj=tweet_obj, 
				content=req_data.get('content'), 
				image=response.get('data').get('link'), 
				image_delete_hash = response.get('data').get('deletehash')
			)
		else :
			return Response({"message": "Something went wrong while uploading image. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	else:
		new_tweet = Tweet.objects.create(user=Request.user, retweet_obj=tweet_obj, content=req_data.get('content'))
	tweet_serializer = TweetCreateSerializer(new_tweet)
	return Response(tweet_serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_api(Request, *args, **kwargs):
	final_data = Request.data
	if 'image' in Request.data:
		response = image_upload(Request.data.get('image'))
		if response.get('status') == 200:
			final_data['image'] = response.get('data').get('link')
			final_data['image_delete_hash'] = response.get('data').get('deletehash')
		else:
			return Response({"message": "Something went wrong while uploading image. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	serializer = TweetCreateSerializer(data=final_data)
	if serializer.is_valid(raise_exception=True):
		serializer.save(user=Request.user)
		return Response(serializer.data, status=status.HTTP_200_OK)
	return Response({"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_feed(Request, *args, **kwargs):
	user = Request.user
	following_list = user.followings.values_list('id', flat=True)
	tweet_list = Tweet.objects.filter(Q(user__id__in = following_list) | Q(user = user)).order_by('-timestamp')
	serializer = TweetDetailSerializer(tweet_list, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def tweets_by_user(Request, user_id, *args, **kwargs):
	user_obj = User.objects.filter(id=user_id)
	if not user_obj.exists():
		return Response({"message": "Invalid User id"}, status=status.HTTP_404_NOT_FOUND)
	tweet_list = user_obj.first().tweet_set.order_by('-timestamp')
	serializer = TweetDetailSerializer(tweet_list, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def tweets_by_username(Request, user_name, *args, **kwargs):
	user_obj = User.objects.filter(user_name=user_name)
	if not user_obj.exists():
		return Response({"message": "Invalid Username"}, status=status.HTTP_404_NOT_FOUND)
	tweet_list = user_obj.first().tweet_set.order_by('-timestamp')
	serializer = TweetDetailSerializer(tweet_list, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def all_tweet_api(Request, *args, **kwargs):
# 	tweet_list = Tweet.objects.all().order_by("-timestamp")
# 	serializer = TweetDetailSerializer(tweet_list, many=True, context={"user_name": Request.user})
# 	return Response(serializer.data, status=status.HTTP_200_OK)
