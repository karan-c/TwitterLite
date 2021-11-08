from django.contrib import admin
from django.urls import path, include

from tweets.views import (home_view)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', home_view),
    path('admin/', admin.site.urls),
    path('api/', include(('tweets.urls', "tweets"), namespace='tweets')),
    path('api/', include(('users.urls', "users"), namespace='users')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
