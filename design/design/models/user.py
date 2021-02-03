from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from design.settings import HTTP_TYPE, DOMAIN, DEBUG
from django.urls import reverse


from design.helper import normalize_email

class CustomUserManager(BaseUserManager):

    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')

        email = normalize_email(email).normalized_address
        print(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None

    email = models.EmailField('email address', unique=True)
    
    is_designer = models.BooleanField('designer status', default=False)
    is_business = models.BooleanField('business status', default=False)
    
    affiliation = models.CharField(max_length=128, default='', help_text="To which institute are you affiliated?")
    is_email_activated = models.BooleanField('email verified', default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def generate_activation_url(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.pk))
        token = default_token_generator.make_token(self)
        return "{}://{}{}".format(HTTP_TYPE, DOMAIN,reverse('user_activate', kwargs={'uidb64': uidb64, 'token':token}))

    def check_token(self, token):
        return default_token_generator.check_token(self, token)

    def completed_registration(self):
        if self.is_business:
            return self.businessuser.is_business_complete
        elif self.is_designer:
            return self.designeruser.is_designer_complete
        return False





class DesignerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    is_designer_complete = models.BooleanField('designer registration complete', default=False)
    years_experience = models.IntegerField('years of experience', default=0)


class BusinessUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    business_name = models.CharField(max_length=128, default='', help_text="Enter the name of your company")
    is_business_complete = models.BooleanField('business registration complete', default=False)





