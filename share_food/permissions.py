from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    '''
    Only authenticated users and admins can access the API.
    Admins can perform all actions.
    '''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    Only authenticated users and admins can access the user profile.
    Admins can modify profiles, while authenticated users can modify their own profiles.
    '''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return False
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or obj.user.is_staff


# class IsOwnerOrReadOnly(permissions.BasePermission):
#     '''
#     Only authenticated users and admins can access the user profile.
#     Admins can modify profiles, while authenticated users can modify their own profiles.
#     '''

#     def has_permission(self, request, view):
#         # Allow read-only actions for everyone
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Allow authenticated users to perform write actions
#         return bool(request.user and request.user.is_authenticated)

#     def has_object_permission(self, request, view, obj):
#         # Allow read-only actions for everyone
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Allow the user to modify their own profile or admin to modify any profile
#         return obj.user == request.user or request.user.is_staff
