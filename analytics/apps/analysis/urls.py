from django.urls import path

from apps.analysis import views


app_name = 'analysis'

urlpatterns = [
    path('', views.AnalysisView.as_view(), name='analysis'),
]
