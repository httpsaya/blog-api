import logging

logger = logging.getLogger('debug requests')

class DebugRequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(
            'Request: %s %s | User %s',
            request.method,
            request.get_full_path(),
            request.user if request.user.is_auhenticated else "Anonymouse"
        )

        response = self.get_response(request)
        return response