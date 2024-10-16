from django.urls import path, include
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()

router.register('profiles', views.UserProfileViewSet, basename='userprofile')
router.register('food-items', views.FoodItemViewSet, basename='food-item')
router.register('transactions', views.TransactionViewSet,
                basename='transaction')
router.register('messages', views.MessageViewSet, basename='message')
router.register('notifications', views.NotificationViewSet,
                basename='notification')

transactions_router = routers.NestedSimpleRouter(
    router, 'transactions', lookup='transaction')
transactions_router.register('reviews', views.ReviewViewSet, basename='review')

urlpatterns = [
    # path('profiles/', views.UserProfileViewSet.as_view()),
    # path('profiles/<int:pk>', views.UserProfileDetailView.as_view()),
    path('', include(router.urls)),
    path('', include(transactions_router.urls)),
]

urlpatterns += router.urls
urlpatterns += transactions_router.urls
