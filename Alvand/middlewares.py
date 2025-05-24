from django.shortcuts import redirect
from django.urls import reverse
from . import checkLicense
# from .views import getHWID

class LicenseCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if not request.path.startswith(reverse('license')):
        #     if not checkLicense.checkLicenses():
        #         return redirect(reverse('license'))
        response = self.get_response(request)
        return response
