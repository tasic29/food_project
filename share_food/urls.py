from django.urls import path, include
from rest_framework_nested import routers
from . import views


# class APIRootView()


router = routers.DefaultRouter()

router.register('food-items', views.FoodItemViewSet, basename='food-item')
router.register('transactions', views.TransactionViewSet,
                basename='transaction')

transactions_router = routers.NestedSimpleRouter(
    router, 'transactions', lookup='transaction')
transactions_router.register('reviews', views.ReviewViewSet, basename='review')

urlpatterns = [
    path('profiles/', views.UserProfileListView.as_view()),
    path('profiles/<int:pk>', views.UserProfileDetailView.as_view()),
    path('', include(router.urls)),
    path('', include(transactions_router.urls)),
]

urlpatterns += router.urls
urlpatterns += transactions_router.urls
