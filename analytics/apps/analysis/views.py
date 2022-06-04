from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView

from apps.analysis.models import Analysis


class AnalysisView(ListView):
    """This view represents All users's Analysis instance"""
    model = Analysis
    # template_name: '.../some.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        # context =  super(self, ListView).get_context_data(**kwargs)
        context =  super().get_context_data(**kwargs)
        context['data'] = 'Some data'

    def get(self, request: object, *args: set, **kwargs: dict) -> object:
        """Override default 'get' method"""
        # return super().get(request, *args, **kwargs)
        return JsonResponse(data=self.get_context_data(), safe=False)
