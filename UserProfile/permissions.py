from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):

    message = "You cannot change other users data"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.username == view.kwargs['username']

       
            