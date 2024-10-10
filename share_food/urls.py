from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('food-items', views.FoodItemViewSet, basename='food-item')

urlpatterns = [
    path('profile/', views.UserProfileListView.as_view()),
    path('profile/<int:pk>', views.UserProfileDetailView.as_view()),
]

urlpatterns += router.urls
