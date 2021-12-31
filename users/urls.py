from django.urls import path

from users.views import follow_user, get_followers_list, get_followings_list, register_user, update_user, user_details

urlpatterns = [
    path('register-user/', register_user),
    path('user/<int:user_id>/', user_details),
    path('update-user/', update_user),
    path('follow-user/', follow_user),
    path('followers-list/<int:user_id>', get_followers_list),
    path('followings-list/<int:user_id>', get_followings_list)
]