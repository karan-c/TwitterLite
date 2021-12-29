from django.urls import path

from users.views import register_user, update_user, user_details

urlpatterns = [
    path('register-user/', register_user),
    path('user/<int:user_id>/', user_details),
    path('update-user/', update_user)
]