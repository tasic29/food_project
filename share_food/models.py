from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from django.contrib import admin
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=150)
    profile_picture = models.ImageField(
        blank=True, null=True, upload_to='images')
    bio = models.TextField(blank=True, null=True)
    rating = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class FoodItem(models.Model):
    CATEGORY_FRUIT = 'fruit'
    CATEGORY_VEGETABLE = 'vegetable'
    CATEGORY_BAKED_GOODS = 'baked_goods'
    CATEGORY_DAIRY = 'dairy'
    CATEGORY_MEAT = 'meat'
    CATEGORY_SEAFOOD = 'seafood'
    CATEGORY_BEVERAGES = 'beverages'
    CATEGORY_GRAINS = 'grains'
    CATEGORY_PREPARED_MEALS = 'prepared_meals'
    CATEGORY_SNACKS = 'snacks'
    CATEGORY_OTHER = 'other'

    CATEGORY_CHOICES = [
        (CATEGORY_FRUIT, 'Fruit'),
        (CATEGORY_VEGETABLE, 'Vegetable'),
        (CATEGORY_BAKED_GOODS, 'Baked Goods'),
        (CATEGORY_DAIRY, 'Dairy'),
        (CATEGORY_MEAT, 'Meat'),
        (CATEGORY_SEAFOOD, 'Seafood'),
        (CATEGORY_BEVERAGES, 'Beverages'),
        (CATEGORY_GRAINS, 'Grains'),
        (CATEGORY_PREPARED_MEALS, 'Prepared Meals'),
        (CATEGORY_SNACKS, 'Snacks'),
        (CATEGORY_OTHER, 'Other'),
    ]

    def default_available_until(self):
        return timezone.now() + timedelta(days=3)

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_OTHER)
    is_available = models.BooleanField(default=True)
    pickup_location = models.CharField(max_length=300)
    available_until = models.DateTimeField(
        default=default_available_until)
    image = models.ImageField(
        blank=True, null=True, upload_to='images')
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title


class Transaction(models.Model):

    TRANSACTION_STATUS_PENDING = 'P'
    TRANSACTION_STATUS_DELIVERED = 'D'
    TRANSACTION_STATUS_CANCELED = 'C'
    TRANSACTION_STATUS_CHOICES = [
        (TRANSACTION_STATUS_PENDING, 'Pending'),
        (TRANSACTION_STATUS_DELIVERED, 'Delivered'),
        (TRANSACTION_STATUS_CANCELED, 'Canceled')
    ]

    food_item = models.ForeignKey(
        FoodItem, on_delete=models.PROTECT, related_name='transactions')
    food_giver = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, related_name='given_transactions')
    food_receiver = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, related_name='received_transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    pickup_time = models.DateTimeField()
    status = models.CharField(
        max_length=1, choices=TRANSACTION_STATUS_CHOICES, default=TRANSACTION_STATUS_PENDING)
    rating_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)

    def clean(self):
        if self.food_giver == self.food_receiver:
            raise ValidationError(
                'The food giver and receiver cannot be the same person')
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.food_item} - {self.food_giver} to {self.food_receiver}'


class Review(models.Model):
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, related_name='written_reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, related_name='sent_messages')
    receiver = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, related_name='received_messages')
    content = models.TextField(max_length=500)
    sent_at = models.DateTimeField(auto_now_add=True)

    # def clean(self):
    #     if self.sender == self.receiver:
    #         raise ValidationError(
    #             'Message sender and receiver can not be the same person')
    #     super().clean()

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(*args, **kwargs)


class Notification(models.Model):
    NOTIFICATION_TYPE_NEW_MESSAGE = 'new_message'
    NOTIFICATION_TYPE_NEW_FOOD_ITEM = 'new_food_item'
    NOTIFICATION_TYPE_TRANSACTION_UPDATE = 'transaction_update'
    NOTIFICATION_TYPE_REVIEW_RECEIVED = 'review_received'
    NOTIFICATION_TYPE_OTHER = 'other'

    NOTIFICATION_TYPE_CHOICES = [
        (NOTIFICATION_TYPE_NEW_MESSAGE, 'New Message'),
        (NOTIFICATION_TYPE_NEW_FOOD_ITEM, 'New Food Item'),
        (NOTIFICATION_TYPE_TRANSACTION_UPDATE, 'Transaction Update'),
        (NOTIFICATION_TYPE_REVIEW_RECEIVED, 'Review Received'),
        (NOTIFICATION_TYPE_OTHER, 'Other'),
    ]

    recipient = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(
        max_length=50, choices=NOTIFICATION_TYPE_CHOICES, default=NOTIFICATION_TYPE_NEW_MESSAGE)
    message = models.TextField(default='')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.recipient.user.username} - {self.get_notification_type_display()}"

    class Meta:
        ordering = ['-created_at']
