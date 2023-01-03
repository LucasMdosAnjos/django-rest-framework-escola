from rest_framework import permissions
from django.http.request import HttpRequest
class EhSuperUser(permissions.BasePermission):
    def has_permission(self, request:HttpRequest, view):
        if request.method == 'DELETE':
            if request.user.is_superuser:
                return True
            return False
        return True