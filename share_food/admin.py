from django.contrib import admin
from .models import UserProfile, FoodItem, Transaction, Review, Message, Notification


class RatingFilter(admin.SimpleListFilter):
    title = 'rating'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('>4', '4+   stars'),
            ('<4', '4-   stars')
        ]

    def queryset(self, request, queryset):
        if self.value() == '>4':
            return queryset.filter(rating__gt=4)
        elif self.value() == '<4':
            return queryset.filter(rating__lt=4)
        return queryset


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['id', 'first_name', 'last_name', 'location', 'rating']
    list_per_page = 10
    list_filter = [RatingFilter]
    search_fields = ['user__first_name', 'user__last_name']
    list_select_related = ['user']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['owner']
    list_display = ['id', 'title', 'category',
                    'is_available', 'pickup_location', 'available_until', 'owner']
    list_per_page = 10
    search_fields = ['title', 'category']
    list_filter = ['category', 'is_available']
