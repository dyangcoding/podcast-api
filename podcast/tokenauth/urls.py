from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.email_post, name='login'),
    path('login/token_post/', views.token_post, name='login-token'),
    path('logout/', views.logout, name='logout'),
]