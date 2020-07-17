from django.contrib.auth.views import LogoutView
from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    # CRUD for quizzes
    path('quiz/<int:quiz_pk>/delete/', views.quiz_delete, name='quiz_delete'),
    path('quiz/<int:quiz_pk>/change/', views.quiz_change, name='quiz_change'),
    path('quiz/add/', views.quiz_add, name='quiz_add'),
    path('quiz/<int:pk>/passing', views.passing_quiz, name='passing_quiz'),
    path('quiz/<int:pk>/question/add/', views.question_add, name='question_add'),
    path('profile/quiz/<int:pk>/', views.profile_quiz_detail, name='profile_quiz_detail'),
    path('quiz/<int:pk>/', views.detail_quiz, name='detail_quiz'),
    # Crud for comments
    path('quiz/<int:quiz_pk>/delete_comment/<int:pk>/', views.comment_delete, name='comment_delete'),
    path('quiz/<int:quiz_pk>/change_comment/<int:pk>/', views.comment_change, name='comment_change'),

    # Profile user
    path('account/profile/', views.profileView, name='profile'),
    path('profile/users/quizes/', views.users_quizes, name='users_quizes'),
    path('profile/update/<int:pk>/', views.profile_change, name='profile_update'),

    # Register/auth users
    path('login/', views.login_page, name='login'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('register/', views.registerView, name='register'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),

    # main page
    path('', views.index, name='index'),
]
