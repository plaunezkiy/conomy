from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsParty(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in (obj.sender.owner, obj.recipient.owner)
