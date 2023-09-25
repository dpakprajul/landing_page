from django.urls import path
from . import views

urlpatterns = [
    path('parse-wiki-data/', views.parse_wiki_data, name='parse_wiki_data'),
]
