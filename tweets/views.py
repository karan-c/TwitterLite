from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import render

from tweets.models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
	return render(request=request, template_name="pages/home.html", status=200, context={})

def all_tweet_view(request, *args, **kwargs):
		res_tweet = Tweet.objects.get(id=3)

		return JsonResponse(res_tweet)

def tweet_detail_view(request, tweet_id, *args, **kwargs):
		res = {
				"id": tweet_id,
		}
		status = 200
		try: 
			tweet_obj = Tweet.objects.get(id=tweet_id)
			res['content'] = tweet_obj.content
		except:
			status = 404
			res['message'] = "Tweet not found"
		
		return JsonResponse(res, status=status)