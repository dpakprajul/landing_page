from django.urls import path
from . import views #import views.py from home app

urlpatterns = [
    path('',views.HomeView.as_view(), name='home'),  #use home function inside views.py')
    path('authorized',views.AuthorizedView.as_view()),  #use home function inside views.py')
    path('login',views.LoginInternalView.as_view(), name='login'),  #use home function inside views.py')
    path('logout',views.LogoutInternalView.as_view(), name='logout'),  #use home function inside views.py')
    path('signup',views.SignupView.as_view(), name='signup'),  #use home function inside views.py'
]


