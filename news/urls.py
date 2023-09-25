# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_page, name='news_page'),
]
