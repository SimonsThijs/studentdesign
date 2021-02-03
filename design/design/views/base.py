from django.views import View
from django.shortcuts import reverse

from design.settings import APPLICATION_NAME, LOGIN_URL


class BaseView(View):
    """These views are used to handle recurring elements of the application and their context. 
        A good example is the navigation bar"""

    # active navbar item
    active = 'None'

    # title of the page, if the title is not given default to this
    title = 'Student Design'

    def get_context(self,request):
        self.context['application_name'] = APPLICATION_NAME

        items = [ ('Home', reverse('homepage')),
                ('About', '#'),
                ('Contact', '#')]

        self.context['navbar_items'] = items
        self.context['active'] = self.active
        self.context['title'] = self.title

        self.context['navbar_right'] = list()


        if request.user.is_authenticated:
            self.context['navbar_items'].append(('Database', reverse('database_filter')))
            self.context['navbar_right'] = [('Logout', reverse('user_logout')),]
            if request.user.is_business:
                self.context['navbar_style'] = 'business'
            elif request.user.is_designer:
                self.context['navbar_style'] = 'designer'
                self.context['navbar_right'].append(('Upload', reverse('project_upload')))


        else:
            self.context['navbar_style'] = 'prelogin'
            self.context['navbar_right'] = [('Login', LOGIN_URL),
            ('Signup (Business)', reverse('business_registration')),
            ('Signup (Designer)', reverse('designer_registration')),]


    def dispatch(self, request, *args, **kwargs):
        self.context = dict()
        self.get_context(request)
        return super().dispatch(request, *args, **kwargs)

        













