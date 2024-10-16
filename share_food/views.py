from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .permissions import IsAdminOrOwner, IsOwnerOrReadOnly, MessagePermission, ReviewPermission, TransactionPermission

from .serializers import (FoodItemSerializer,
                          MessageSerializer,
                          NotificationSerializer,
                          ReviewSerializer,
                          TransactionSerializer,
                          UserProfileSerializer)
from .models import (FoodItem,
                     Notification,
                     Review,
                     Transaction,
                     UserProfile,
                     Message)


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminOrOwner]

    @action(detail=False, methods=['GET', 'PUT', 'DELETE'])
    def me(self, request):
        owner = UserProfile.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = UserProfileSerializer(owner)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(owner, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            owner.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(method='POST')


class FoodItemViewSet(ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(owner=user_profile)


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [TransactionPermission]

    def get_queryset(self):
        if self.request.method == 'GET':
            return Transaction.objects.all()
        return Transaction.objects.filter(food_giver=self.request.user.userprofile)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['food_giver'] = self.request.user.userprofile
        return context


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPermission]

    def get_queryset(self):
        return Review.objects.select_related('reviewer').filter(transaction_id=self.kwargs['transaction_pk'])

    def get_serializer_context(self):
        return {
            'reviewer_id': self.request.user.userprofile.id,
            'transaction_id': self.kwargs['transaction_pk'],
        }


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [MessagePermission]

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        if self.request.user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(Q(sender=user_profile) | Q(receiver=user_profile))

    def get_serializer_context(self):
        return {
            'sender_id': self.request.user.userprofile.id,
        }


class NotificationViewSet(ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Notification.objects.all()

        return Notification.objects.filter(recipient=self.request.user.userprofile)
