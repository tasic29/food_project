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


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['food_item', 'food_giver', 'food_receiver']
    list_display = ['id', 'food_item', 'food_giver', 'food_receiver',
                    'created_at', 'pickup_time', 'status', 'rating_given']
    list_filter = ['status']
    search_fields = ['food_item__title', 'food_giver__user__first_name', 'food_giver__user__last_name',
                     'food_receiver__user__first_name', 'food_receiver__user__last_name']
    list_per_page = 10
    list_editable = ['status', 'pickup_time']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields = ['reviewer']
    list_display = ['id', 'transaction', 'reviewer',
                    'rating', 'comment', 'created_at']
    list_filter = [RatingFilter]
    list_select_related = [
        'transaction',
        'transaction__food_item',
        'transaction__food_giver',
        'transaction__food_receiver',
        'reviewer__user'
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['sender']
    list_display = ['id', 'sender', 'receiver', 'content', 'sent_at']
    list_select_related = ['sender', 'receiver']
    search_fields = [
        'sender__user__first_name',
        'sender__user__last_name',
        'receiver__user__first_name',
        'receiver__user__last_name',
    ]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['recipient']
    list_display = ['id', 'recipient', 'notification_type',
                    'message', 'is_read', 'created_at']
    list_filter = ['is_read']
