from django.urls import path
from .views import (
    view_users,
    create_users,
    user_details,
    view_auction_bids,
    view_auctions,
    view_user_bids,
    create_bids,
    auction_details,
)

urlpatterns = [
    # view all users
    path("users/", view_users),
    # create users
    path("users/create/", create_users),
    # view user details, delete user , update user
    path("users/<int:pk>/", user_details),
    # view bids for an action
    path("auctions/bids/<int:pk>/", view_auction_bids),
    # view user bids
    path("users/me/bids/", view_user_bids),
    # create bids
    path("auctions/create-bid/", create_bids),
    # view auctions and admin able to create an auction
    path("auctions/", view_auctions),
    # auction details, update an auction , delete auction
    path("auctions/<int:pk>/", auction_details),
]
