from rest_framework import serializers

from .models import FoodItem, UserProfile


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
    owner_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = FoodItem
        fields = ['id', 'title', 'description', 'category', 'is_available',
                  'pickup_location', 'available_until', 'image', 'owner_id']

    def create(self, validated_data):
        owner_id = self.context['owner_id']
        return FoodItem.objects.create(owner_id=owner_id, **validated_data)


# class TransactionSerializer
