# Django-Middleware-0x03/chats/middleware.py

from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden

# Middleware 1: Logs each user request
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        
        # Log to file
        with open("requests.log", "a") as f:
            f.write(log_message)
        
        response = self.get_response(request)
        return response

# Middleware 2: Restrict access to chat between 6 PM and 9 PM
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Deny access if time is before 6 PM (18) or after 9 PM (21)
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Chat access is restricted between 9 PM and 6 PM.")
        
        response = self.get_response(request)
        return response
