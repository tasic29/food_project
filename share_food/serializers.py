from rest_framework import serializers

from .models import FoodItem, Review, Transaction, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user_id', 'full_name', 'location', 'phone_number',
                  'profile_picture', 'bio', 'rating']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class FoodItemSerializer(serializers.ModelSerializer):
    # owner_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = FoodItem
        fields = ['id', 'title', 'description', 'category', 'is_available',
                  'pickup_location', 'available_until', 'image']


class TransactionSerializer(serializers.ModelSerializer):
    food_giver_id = serializers.IntegerField(read_only=True)
    food_receiver_id = serializers.IntegerField()

    class Meta:
        model = Transaction
        fields = ['id', 'food_item', 'food_giver_id', 'food_receiver_id',
                  'created_at', 'pickup_time', 'status', 'rating_given']

    def create(self, validated_data):
        food_giver = self.context['food_giver']
        validated_data.pop('food_giver_id', None)
        return Transaction.objects.create(food_giver=food_giver, **validated_data)

    def validate(self, data):
        food_giver = self.context['food_giver']
        if food_giver == data['food_receiver_id']:
            raise serializers.ValidationError(
                'Food giver and receiver cannot be the same person.')
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['transaction', 'reviewer', 'rating', 'comment']
