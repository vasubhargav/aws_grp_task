from rest_framework.permissions import BasePermission
class  landlordPermission(BasePermission):
    def has_permission(self, request, view):
        message = "landlord permission is valid only for landlord users"
        return (request.user.is_authenticated and request.user.role == 'landlord')
class  tenantPermission(BasePermission):
    def has_permission(self, request, view):
        message = "tenant permission is valid only for tenant users"
        return (request.user.is_authenticated and request.user.role == 'tenant')
class landlordOrTenantPermission(BasePermission):
    def has_permission(self, request, view):
        message = "landlord or tenant permission is valid only for landlord or tenant users"
        return (request.user.is_authenticated and (request.user.role == 'landlord' or request.user.role == 'tenant'))