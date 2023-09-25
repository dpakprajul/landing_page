from django.urls import path
from . import views

urlpatterns = [
    path('display-data/', views.display_data, name='display_data'),
    path('highest-data/', views.highest_data, name='highest_data'),
    path('high-priority-notes/', views.high_priority_notes, name='high_priority_notes'),
    
]
