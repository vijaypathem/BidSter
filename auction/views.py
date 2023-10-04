from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import UsersSerializer, BidSerializer, AuctionSerializer

from .models import Auction, Bid


# Create your views here.


# view all users
@api_view(["GET"])
@permission_classes((IsAdminUser,))
def view_users(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# admin able to do crud on users
@api_view(["GET", "PUT", "DELETE"])
@permission_classes((IsAdminUser,))
def user_details(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "GET":
        serializer = UsersSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PUT":
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)
    if request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# admin able to create users
@api_view(["POST"])
@permission_classes((IsAdminUser,))
def create_users(request):
    if request.method == "POST":
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# all users able to see all the auctions
@api_view(["GET", "POST"])
@permission_classes(())
def view_auctions(request):
    if request.method == "GET":
        auctions = Auction.objects.filter(status="open")
        serializer = AuctionSerializer(auctions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.user.is_staff():
        if request.method == "POST":
            serializer = AuctionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# admin able to do CRUD operations on Auctions
@api_view(["GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticated,))
def auction_details(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    if request.method == "GET":
        serializer = AuctionSerializer(auction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if not request.user.is_staff():
        return Response(
            {"detail": "you are not allowed"}, status=status.HTTP_400_BAD_REQUEST
        )
    if request.method == "PUT":
        serializer = AuctionSerializer(auction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == "DELETE":
        auction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# manager able to see all bids of an auction
@api_view(["GET"])
@permission_classes((IsAdminUser,))
def view_auction_bids(request, pk):
    if request.method == "GET":
        auction_bids = get_list_or_404(Bid, auction=pk)
        serializer = BidSerializer(auction_bids, many=True)
        if serializer.data:
            return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# user able to see all his bids
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def view_user_bids(request):
    if request.method == "GET":
        user_bids = get_list_or_404(Bid, bidder=request.user)
        serializer = BidSerializer(user_bids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# users able to bid auction
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_bids(request):
    if request.method == "POST":
        serializer = BidSerializer(data=request.data)
        serializer.initial_data["bidder"] = request.user.id
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)
