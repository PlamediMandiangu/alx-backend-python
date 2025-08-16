from django.http import HttpResponseForbidden
from time import time
from datetime import datetime

# 1️⃣ Restrict Access by Time
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/chats/'):
            current_hour = datetime.now().hour
            if current_hour >= 21 or current_hour < 6:
                return HttpResponseForbidden("Chat access is restricted at this time.")
        return self.get_response(request)

# 2️⃣ Offensive Language / Rate Limit
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_timestamps = {}

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chats/'):
            ip = request.META.get('REMOTE_ADDR')
            now = time()
            timestamps = self.ip_timestamps.get(ip, [])
            timestamps = [t for t in timestamps if now - t < 60]
            if len(timestamps) >= 5:
                return HttpResponseForbidden("Too many messages. Please wait a minute.")
            timestamps.append(now)
            self.ip_timestamps[ip] = timestamps
        return self.get_response(request)

# 3️⃣ Role Permission
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/chats/'):
            user = getattr(request, 'user', None)
            if not user or not user.is_authenticated:
                return HttpResponseForbidden("You must be logged in to access this resource.")
            user_role = getattr(user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to perform this action.")
        return self.get_response(request)

# 4️⃣ Request Logging
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Request path: {request.path}")
        response = self.get_response(request)
        return response
