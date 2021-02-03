from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from datetime import datetime

from design.models.project import Project
from design.forms.project import ProjectForm
from design.views.base import BaseView
from design.views.accessviews import CustomAccessMixin


class ProjectUpload(CustomAccessMixin, BaseView):
    """docstring for ClassName"""
    designer_access_only = True

    title = 'Upload'
    def post(self, request):
        form = ProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            project = form.save()
            # materials = form.cleaned_data.get("materials")
            # post.materials.set(materials)
            project.save()


            return HttpResponseRedirect(reverse('homepage'))
        else:
            self.context.update({'form': form})
            return render(request, 'project/upload.html', self.context)

        self.context.update({'form': form})
        return render(request, 'project/upload.html', self.context)

    def get(self, request):
        form = ProjectForm()
        self.context.update({'form': form})
        return render(request, 'project/upload.html', self.context)
