from django.shortcuts import render

from design.views.base import BaseView
from design.views.accessviews import CustomAccessMixin

class DatabaseFilter(CustomAccessMixin, BaseView):
	"""docstring for DatabaseFilter"""
	title = 'Database'
	active = 'Database'
	def get(self, request):
		return render(request, 'database/filter.html', self.context)
