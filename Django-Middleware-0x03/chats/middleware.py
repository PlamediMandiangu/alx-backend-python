# Django-Middleware-0x03/chats/middleware.py
from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only enforce on certain paths (e.g., /chats/secure/)
        if request.path.startswith('/chats/'):
            user = getattr(request, 'user', None)
            
            if not user or not user.is_authenticated:
                return HttpResponseForbidden("You must be logged in to access this resource.")
            
            # Assuming `role` is a field on your User model
            user_role = getattr(user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to perform this action.")
        
        return self.get_response(request)
