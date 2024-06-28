import logging
from logging.handlers import TimedRotatingFileHandler

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Create a logger
        self.logger = logging.getLogger('django.request')

        # Create a handler that writes log records to a log file
        handler = TimedRotatingFileHandler('logs/django.log', when='midnight', backupCount=7)

        # Use a formatter to include the timestamp in the log records
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)

    def __call__(self, request):
        # Log the incoming request
        self.logger.info(f'Incoming request: {request.method} {request.get_full_path()}')

        # Call the next middleware or the view
        response = self.get_response(request)

        # Log the outgoing response
        self.logger.info(f'Outgoing response: {response.status_code}')

        return response