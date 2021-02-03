"""design URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import homepage, project, user_registration, user_loginlogout, database


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage.Index.as_view(), name='homepage'),

    path('database', database.DatabaseFilter.as_view(), 
    	name='database_filter'),

    path('project/upload', project.ProjectUpload.as_view(), 
    	name='project_upload'),

    path('user/designerregistration', user_registration.DesignerRegistration.as_view(), 
    		name='designer_registration'),

    path('user/completedesignerregistration', user_registration.CompleteDesignerRegistration.as_view(), 
    		name='designer_registration_complete'),

    path('user/completebusinessregistration', user_registration.CompleteBusinessRegistration.as_view(), 
    		name='business_registration_complete'),

    path('user/businessregistration', user_registration.BusinessRegistration.as_view(), 
    		name='business_registration'),

    path('user/completeregistration', user_registration.complete_registration, 
    		name='complete_registration'),

    path('user/activate/<uidb64>/<token>/',user_registration.VerifyEmail.as_view(), 
    		name='user_activate'),

    path('user/login', user_loginlogout.Login.as_view(), 
    		name='user_login'),

   	path('user/logout', user_loginlogout.Logout.as_view(), 
    		name='user_logout'),

   	path('user/changepassword', user_loginlogout.PasswordChange.as_view(), 
    		name='change_password'),

   	path('user/resetpassword', user_loginlogout.PasswordReset.as_view(), 
    		name='password_reset'),

   	path('user/resetpassworddone', user_loginlogout.PasswordResetDone.as_view(), 
    		name='password_reset_done'),

   	path('user/resetpassword/<uidb64>/<token>/', user_loginlogout.PasswordResetConfirm.as_view(),
   			name='password_reset_confirm'),

   	path('user/resetpasswordcomplete/', user_loginlogout.PasswordResetComplete.as_view(),
   			name='password_reset_complete')

]



