from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet
from . import views
from django.contrib import admin


router = DefaultRouter()
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('notes',views.NotesListView.as_view(), name='notes.list'),
    path('notes/<int:pk>',views.NotesDetailView.as_view(), name='notes.detail'),
    path('notes/<int:pk>/edit',views.NotesUpdateView.as_view(), name='notes.edit'),
    path('notes/<int:pk>/delete',views.NotesDeleteView.as_view(), name='notes.delete'),
    path('notes/new',views.NotesCreateView.as_view(), name='notes.new'),
    path('', include(router.urls)),
    
]

