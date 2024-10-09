from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user_id', 'full_name', 'location', 'phone_number',
                  'profile_picture', 'bio', 'rating']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
