from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.http import HttpResponseForbidden


class CustomAccessMixin(AccessMixin):
    """custom verification if user is authenticated, currently only handles login and email verification. 
    In the future it will also handle subscription status."""
    allow_uncompleted = False
    desinger_access_only = False
    business_access_only = False

    def handle_access(self, request):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif not request.user.is_email_activated:
            return redirect('homepage') #TODO: add the 'your email is not verified' page
        elif not request.user.completed_registration() and not self.allow_uncompleted:
            if request.user.is_business:
                return redirect('business_registration_complete')
            elif request.user.is_designer:
                return redirect('designer_registration_complete')
        elif self.desinger_access_only and not request.user.is_designer:
            return HttpResponseForbidden()
        elif self.business_access_only and not request.user.is_business:
            return HttpResponseForbidden()

        return

    def dispatch(self, request, *args, **kwargs):
        response = self.handle_access(request)
        if response:
            return response
        return super().dispatch(request, *args, **kwargs)



        










