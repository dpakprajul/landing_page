# exportdata/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('export-json/', views.export_data_to_json, name='export_json_data'),
]
