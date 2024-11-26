from rest_framework.permissions import BasePermission
from django.conf import settings

KnowApiTokens = {
    'SurtidorApi': 'k1l2m3n4o5p6q7r8s9t0',
    'RefineriaApi': 'u1v2w3x4y5z6a7b8c9d0'
}
class IsKnowApi(BasePermission):
    def has_permission(self, request, view):
        api_token = request.headers.get('APITOKEN')
        if not api_token:
            return False
        if api_token not in KnowApiTokens.values():
            return False
        return True
