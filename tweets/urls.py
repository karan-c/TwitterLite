from django.urls import path

from .views import all_tweet_api, retweet_api, tweet_create_api, tweet_delete_api, tweet_detail_api, tweet_like_api

urlpatterns = [
    path('tweet/', all_tweet_api),
    path('tweet/<int:tweet_id>/', tweet_detail_api),
    path('delete-tweet/<int:tweet_id>/', tweet_delete_api),
    path('create-tweet/', tweet_create_api),
    path('like-tweet/', tweet_like_api),
    path('retweet/', retweet_api),
]