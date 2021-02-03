from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.views import View

from datetime import datetime

from design.models.user import User, BusinessUser, DesignerUser
from design.forms.user_registration import DesignerRegistrationForm, UserRegistrationForm, BusinessRegistrationForm
from design.settings import DEBUG
from design.views.accessviews import CustomAccessMixin
from design.views.base import BaseView

def complete_registration(request):
    user = request.user
    if user.is_business and not user.businessuser.is_business_complete:
        return redirect('business_registration_complete')
    elif user.is_designer and not user.designeruser.is_designer_complete:
        return redirect('designer_registration_complete')

    return redirect('homepage')

def send_activation_email(email, url, user):
    mail_subject = 'Activate your account.'
    message = render_to_string('user/user_verification_email.html', {
        'user': user,
        'url': url
    })
    to_email = email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    if not DEBUG:
        email.send()

    return message

class VerifyEmail(BaseView):
    """docstring for VerifyEmail"""
    title = 'Email verified'

    def get(self, request, uidb64, token):
        user = None
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except:
            self.context.update({'message': 'Verification failed'})
            return render(request, 'user/verification_message.html', self.context)

        if user is not None and user.is_email_activated:
            # trying to activate for a second time. activation should only work a single time because we do a login after activation
            self.context.update({'message': 'Already verified'})
            return render(request, 'user/verification_message.html', self.context)
        elif user is not None and user.check_token(token):
            # first time clicking the link and token is correct
            user.is_email_activated = True
            user.save()
            login(request, user)

            # reload the context because user logged in
            self.get_context(request)
            self.context.update({'message': 'You succesfully verified your email'})
            return render(request, 'user/verification_message.html', self.context)
        else:
            # user none or token incorrect
            self.context.update({'message': 'Verification failed'})
            return render(request, 'user/verification_message.html', self.context)


class CompleteBusinessRegistration(CustomAccessMixin, BaseView):
    business_access_only = True
    allow_uncompleted = True

    def get(self, request):
        business_form = BusinessRegistrationForm()

        self.context.update({'name': 'Homepage', 'form': business_form})
        return render(request, 'user/business_registration_complete.html', self.context)   

    def post(self, request):
        business_form = BusinessRegistrationForm(request.POST)
        # check whether it's valid:
        business_valid = business_form.is_valid()
        if business_valid:


            data = business_form.cleaned_data
            data['is_business_complete'] = True
            BusinessUser.objects.filter(user__id=request.user.id).update(**data)

            context = {'name': 'Profile completion', 'message': 'Thanks for registering with us. You are ready to go.'}

            return render(request, 'user/verification_message.html', context)

        self.context.update({'name': 'Homepage', 'form': designer_form})
        return render(request, 'user/business_registration_complete.html', self.context)


class CompleteDesignerRegistration(CustomAccessMixin, BaseView):
    designer_access_only = True
    allow_uncompleted = True

    def get(self, request):
        designer_form = DesignerRegistrationForm()

        self.context.update({'name': 'Homepage', 'form': designer_form})
        return render(request, 'user/designer_registration_complete.html', self.context)   

    def post(self, request):
        designer_form = DesignerRegistrationForm(request.POST)
        # check whether it's valid:
        designer_valid = designer_form.is_valid()
        if designer_valid:


            data = designer_form.cleaned_data
            data['is_designer_complete'] = True
            DesignerUser.objects.filter(user__id=request.user.id).update(**data)

            self.context.update({'name': 'Profile completion', 
                'message': 'Thanks for registering with us. You are ready to go.'})

            return render(request, 'user/verification_message.html', self.context)

        self.context.update({'name': 'Homepage', 'form': designer_form})
        return render(request, 'user/designer_registration_complete.html', self.context)    



class DesignerRegistration(BaseView):
    title = 'Register'
    def get(self, request):
        user_form = UserRegistrationForm()
        self.context.update({'name': 'Homepage', 'user_form': user_form})
        return render(request, 'user/designer_registration.html', self.context)

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        # check whether it's valid:
        user_valid = user_form.is_valid()
        if user_valid:
            email = user_form.cleaned_data.pop('email')
            password = user_form.cleaned_data.pop('password2')
            user_form.cleaned_data.pop('password1')
            extra_attributes = user_form.cleaned_data
            extra_attributes['is_designer'] = True
            user = User.objects.create_user(email, password, **extra_attributes)
            designer = DesignerUser()
            designer.user = user
            designer.save()

            message = send_activation_email(email, user.generate_activation_url(), user)

            self.context.update({'message': 'An email has been sent with a verification link'})
            if DEBUG:
                self.context['message'] = message

            return render(request, 'user/verification_message.html', self.context)

        self.context.update({'user_form': user_form})
        return render(request, 'user/verification_message.html', self.context)


class BusinessRegistration(BaseView):
    active = 'Home'

    def get(self, request):
        user_form = UserRegistrationForm()

        self.context.update({'name': 'Homepage', 'user_form': user_form})
        return render(request, 'user/business_registration.html', self.context)

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        # check whether it's valid:
        if user_form.is_valid():
            email = user_form.cleaned_data.pop('email')
            password = user_form.cleaned_data.pop('password2')
            user_form.cleaned_data.pop('password1')
            extra_attributes = user_form.cleaned_data
            extra_attributes['is_business'] = True
            print(extra_attributes)
            user = User.objects.create_user(email, password, **extra_attributes)
            business = BusinessUser()
            business.user = user
            business.save()

            message = send_activation_email(email, user.generate_activation_url(), user)

            self.context.update({'name': 'Email verification', 
                    'message': 'An email has been sent with a verification link'})
            if DEBUG:
                self.context['message'] = message

            return render(request, 'user/verification_message.html', self.context)
        

        self.context.update({'name': 'Homepage', 'user_form': user_form})
        return render(request, 'user/business_registration.html', self.context)






