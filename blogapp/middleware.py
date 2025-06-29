from django.http import HttpResponseRedirect
from axes.attempts import is_already_locked

class AxesRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == '/accounts/login/' and is_already_locked(request):
            return HttpResponseRedirect('/accounts/locked/')
        return response