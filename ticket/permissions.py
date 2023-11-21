from rest_framework import permissions


class IsnotStaff(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.is_staff:
            return False
        else:
            return True


class IsOwnerOrStuff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return obj.created_by == request.user
