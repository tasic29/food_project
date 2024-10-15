from rest_framework import serializers

from .models import FoodItem, Notification, Review, Transaction, UserProfile, Message


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
    reviewer_id = serializers.IntegerField(read_only=True)
    transaction_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'transaction_id', 'reviewer_id', 'rating', 'comment']

    def validate(self, attrs):
        if not self.context.get('reviewer_id') or not self.context.get('transaction_id'):
            raise serializers.ValidationError(
                'Missing reviewer or transaction information. Are you logged in?')
        return attrs

    def create(self, validated_data):
        reviewer_id = self.context['reviewer_id']
        transaction_id = self.context['transaction_id']
        return Review.objects.create(
            reviewer_id=reviewer_id,
            transaction_id=transaction_id,
            **validated_data
        )


class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(read_only=True)
    receiver_id = serializers.IntegerField()

    class Meta:
        model = Message
        fields = ['id', 'sender_id', 'receiver_id', 'content']

    def create(self, validated_data):
        sender_id = self.context['sender_id']
        if sender_id == validated_data.get('receiver_id'):
            raise serializers.ValidationError(
                'Message sender and receiver cannot be the same person.')
        message = Message.objects.create(sender_id=sender_id, **validated_data)

        # create Notification
        Notification.objects.create(
            recipient=message.receiver,
            notification_type=Notification.NOTIFICATION_TYPE_NEW_MESSAGE,
            message=f'{message.sender.user.first_name} {
                message.sender.user.last_name} sent you a new message.'
        )
        return message


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'notification_type', 'message', 'is_read']
