from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

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
@api_view(["GET"])
@permission_classes(())
def view_auctions(request):
    if request.method == "GET":
        auctions = Auction.objects.all()
        serializer = AuctionSerializer(auctions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# manager able to see all bids


# user able to see all his bids


# admin able to do CRUD operations on Auctions
