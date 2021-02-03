from django.apps import AppConfig


class DesignConfig(AppConfig):
    name = 'design'

    def ready(self):
    	return
        # import blogs.hooks
