from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, GenericAPIView

from .serializers import FoodItemSerializer, ReviewSerializer, TransactionSerializer, UserProfileSerializer
from .models import FoodItem, Review, Transaction, UserProfile


class UserProfileListView(ListAPIView, RetrieveUpdateAPIView, GenericAPIView):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer


class UserProfileDetailView(RetrieveUpdateAPIView, GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


# class UserProfileViewSet(viewsets.ViewSet):

#     def list(self, request):
#         view = UserProfileListView.as_view()
#         return view(request)

#     def retrieve(self, request, pk=None):
#         view = UserProfileDetailView.as_view()
#         return view(request, pk=pk)


class FoodItemViewSet(ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(owner=user_profile)


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['food_giver'] = self.request.user.userprofile
        return context


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.select_related('reviewer').filter(transaction_id=self.kwargs['transaction_pk'])

    def get_serializer_context(self):
        print(self.request.user.id)
        return {
            'reviewer_id': self.request.user.userprofile.id,
            'transaction_id': self.kwargs['transaction_pk'],
        }
