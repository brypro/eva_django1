from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('unlock/', views.unlock_accounts, name='unlock'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # URL para el logout
]
