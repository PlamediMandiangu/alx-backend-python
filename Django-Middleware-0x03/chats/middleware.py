# chats/middleware.py
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Track requests by IP: { ip: [timestamps] }
        self.message_log = {}
        self.time_window = timedelta(minutes=1)
        self.max_messages = 5

    def __call__(self, request):
        if request.method == "POST" and "/chat" in request.path.lower():
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Create list for IP if not exists
            if ip not in self.message_log:
                self.message_log[ip] = []

            # Remove timestamps outside time window
            self.message_log[ip] = [
                t for t in self.message_log[ip] if now - t < self.time_window
            ]

            # Check limit
            if len(self.message_log[ip]) >= self.max_messages:
                return HttpResponseForbidden(
                    "Rate limit exceeded: You can only send 5 messages per minute."
                )

            # Log this message
            self.message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip
