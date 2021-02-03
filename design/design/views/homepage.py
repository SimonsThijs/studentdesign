from django.http import HttpResponse
from django.shortcuts import render

from design.views.base import BaseView


class Index(BaseView):
	title = 'Home'
	active = 'Home'
	def get(self, request):
	    return render(request, 'homepage.html', self.context)