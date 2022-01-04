from django.urls import path

from .views import all_tweet_api, my_feed, retweet_api, tweet_create_api, tweet_delete_api, tweet_detail_api, tweet_like_api, tweets_by_user, tweets_by_username

urlpatterns = [
    path('tweet/', all_tweet_api),
    path('tweet/<int:tweet_id>/', tweet_detail_api),
    path('delete-tweet/<int:tweet_id>/', tweet_delete_api),
    path('create-tweet/', tweet_create_api),
    path('like-tweet/', tweet_like_api),
    path('retweet/', retweet_api),
    path('feed/', my_feed),
    path('tweets-by-user/<int:user_id>/', tweets_by_user),
    path('tweets-by-username/<str:user_name>/', tweets_by_username)
]