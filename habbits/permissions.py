from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user == obj.habit_owner:
            return True

        return False


class IsPrizeOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user == obj.prize_owner:
            return True

        return False
    