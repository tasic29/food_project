from rest_framework import serializers

from .models import FoodItem, Transaction, UserProfile


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
    class Meta:
        model = Transaction
        fields = ['food_item', 'food_receiver',
                  'pickup_time', 'status', 'rating_given']

    def validate(self, data):
        request = self.context.get('request')
        food_giver = request.user.userprofile

        if food_giver == data.get('food_receiver'):
            raise serializers.ValidationError(
                'The food giver and receiver cannot be the same person.'
            )
        return data
