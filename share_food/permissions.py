from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    '''
    Allows authenticated users to list and view profiles.
    Only admins and owners can update or delete their own profiles.
    '''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True

        user = getattr(obj, 'user', None)
        if user is None:
            user = getattr(obj, 'owner', None) and getattr(
                obj.owner, 'user', None)

        return user == request.user


class TransactionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        if view.action == 'rate':
            return obj.food_receiver.user == request.user
        return obj.food_giver.user == request.user


class ReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'POST']:
            return True
        if request.user.is_staff:
            return True
        if request.method in ['PUT', 'DELETE']:
            return obj.reviewer.user == request.user


class MessagePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.sender.user == request.user or obj.receiver.user == request.user or request.user.is_staff
        if request.user.is_staff:
            return True
        return obj.sender.user == request.user
