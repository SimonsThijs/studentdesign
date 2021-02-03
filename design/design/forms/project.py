from django import forms
from django.core.validators import ValidationError

from datetime import datetime

from design.models.project import Project, Material

class MinMaxManyToManyValidator(object):
    def __init__(self, min_, max_):
        self.min = min_
        self.max = max_
        return

    def __call__(self, value):
        n_of_selected = len(value)
        if n_of_selected == 0:
            raise ValidationError(
                'Nothing is selected'
            )
        elif n_of_selected < self.min or n_of_selected > self.max:
            raise ValidationError(
                'Select at least {} item(s) and at most {} items'.format(self.min, self.max)
            )
        return

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'materials']

    title = forms.CharField(label='The title of your project')
    materials = forms.ModelMultipleChoiceField(queryset=Material.objects, validators=[MinMaxManyToManyValidator(1,2),])