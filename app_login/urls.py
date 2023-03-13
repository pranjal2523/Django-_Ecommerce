from django.urls import path
from . import views

app_name = 'app_login'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('user_profile', views.user_profile, name='change_profile'),

]