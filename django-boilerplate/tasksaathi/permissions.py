from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the owner
        if hasattr(obj, 'userId'):
            return obj.userId == request.user
        elif hasattr(obj, 'createdBy'):
            return obj.createdBy == request.user
        return False

class IsCompanyUser(permissions.BasePermission):
    """
    Custom permission to only allow company users to access their company data.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
        
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'companyId'):
            return obj.companyId.userId == request.user
        return obj.userId == request.user