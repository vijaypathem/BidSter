from django.urls import path
from .views import view_users, create_users, user_details

urlpatterns = [
    # view all users
    path("users/", view_users),
    # create users
    path("users/create/", create_users),
    # view user details, delete user , update user
    path("users/<int:pk>/", user_details),
]
