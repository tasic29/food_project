from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, GenericAPIView

from .serializers import UserProfileSerializer
from .models import UserProfile


class UserProfileListView(ListAPIView, RetrieveUpdateAPIView, GenericAPIView):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer


class UserProfileDetailView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
