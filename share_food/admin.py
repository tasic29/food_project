from django.contrib import admin
from .models import UserProfile, FoodItem, Transaction, Review, Message, Notification


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'rating']
    autocomplete_fields = ['user']
