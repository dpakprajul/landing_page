from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
from .models import Notes #Notes is the name of the class in models.py
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from .forms import NotesForm
from rest_framework import viewsets
from .models import Notes
from .serializers import NoteSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
import datetime
from django.utils import timezone

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NoteSerializer

class NotesUpdateView(UpdateView):
    model = Notes
    success_url = '/smart/notes'
    form_class = NotesForm

    def form_valid(self, form):
        # Update the edited timestamp before saving the form
        self.object.edited = timezone.now()
        self.object.save()
        return super().form_valid(form)

class NotesDeleteView(DeleteView):
    model = Notes
    success_url = '/smart/notes'
    

class NotesCreateView(CreateView):
    model = Notes
    success_url = '/smart/notes'
    form_class = NotesForm

    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = 'notes'
    template_name = 'notes/notes_list.html'
    login_url = '/admin'

    def get_queryset(self):
        return self.request.user.notes.all()

class NotesDetailView(DetailView):
    model = Notes
    context_object_name = 'note'
   


    
   



#this def is not needed because we are using class based views
# def detail(request,pk):
#     try:
#         note = Notes.objects.get(pk=pk)
#     except Notes.DoesNotExist:
#         #name the 404 error and render it in error_details.html
        
#         return render(request,'notes/error_details.html')
#     return render(request,'notes/notes_detail.html',{'note':note})
    