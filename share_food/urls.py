from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.UserProfileListView.as_view()),
    path('profile/<int:pk>', views.UserProfileDetailView.as_view()),
]
