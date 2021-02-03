from django.db import models

from datetime import datetime


class Material(models.Model):
	label = models.CharField(max_length=128, default='')

	def __str__(self):
		return self.label

class Project(models.Model):
	title = models.CharField(max_length=128, default='', help_text="Describe your project in one sentence")
	pub_date = models.DateTimeField('date published')
	description = models.CharField(max_length=200)
	materials = models.ManyToManyField(Material)

	def __str__(self):
		return self.title

	def save(self):
		# TODO: figure out how to add the datetime fields last_updated and first_created
		if self.pub_date == None:
			self.pub_date = datetime.now()

		instance = super(Project, self).save()
			
		return instance
