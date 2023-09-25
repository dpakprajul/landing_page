from django.shortcuts import render
from django.http import HttpResponse
#import datetime
from datetime import datetime
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'home/register.html'
    success_url = '/smart/notes'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/smart/notes')
        return super().get(request, *args, **kwargs)

class LogoutInternalView(LogoutView):
    template_name = 'home/logout.html'
    extra_context = {'title':'Logout Page'}

class LoginInternalView(LoginView):
    template_name = 'home/login.html'
    extra_context = {'title':'Login Page'}

class HomeView(TemplateView):
    template_name = 'home/welcome.html'
    extra_context = {'today':datetime.now(), 'name':'Sachin'}

class AuthorizedView(LoginRequiredMixin, TemplateView):
    template_name = 'home/authorized.html'
    login_url = '/admin'


