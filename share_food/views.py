from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, GenericAPIView

from .serializers import FoodItemSerializer, UserProfileSerializer
from .models import FoodItem, UserProfile


class UserProfileListView(ListAPIView, RetrieveUpdateAPIView, GenericAPIView):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer


class UserProfileDetailView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class FoodItemViewSet(ModelViewSet):
    # queryset = FoodItem.objects.select_related('owner__user').all()
    serializer_class = FoodItemSerializer

    def get_queryset(self):
        return FoodItem.objects.filter(owner=self.request.user)

    def get_serializer_context(self):
        return {'owner_id': self.request.user.id}
