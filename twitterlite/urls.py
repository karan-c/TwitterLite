from django.contrib import admin
from django.urls import path

from tweets.views import (all_tweet_api, home_view, retweet_api, tweet_create_api, tweet_delete_api, tweet_detail_api, tweet_like_api)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', home_view),
    path('admin/', admin.site.urls),
    path('tweet/', all_tweet_api),
    path('tweet/<int:tweet_id>/', tweet_detail_api),
    path('delete-tweet/<int:tweet_id>/', tweet_delete_api),
    path('create-tweet/', tweet_create_api),
    path('like-tweet/', tweet_like_api),
    path('retweet/', retweet_api),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
