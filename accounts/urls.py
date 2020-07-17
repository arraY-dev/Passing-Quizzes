from django.contrib.auth.views import LogoutView
from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    # CRUD for quizzes

    # Profile user
    path('account/profile/', views.profileView, name='profile'),
    path('profile/update/<int:pk>/', views.profile_change, name='profile_update'),

    # Register/auth users
    path('login/', views.login_page, name='login'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('register/', views.registerView, name='register'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),

    # main page
    path('', views.index, name='index'),
]
